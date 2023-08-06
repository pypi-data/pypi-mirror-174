import logging
import os
import time
from pathlib import Path
from typing import List, Optional, Tuple

import pandas as pd
import torch
import torchvision.transforms as torch_transforms
from encord.project_ontology.classification_type import ClassificationType
from encord.project_ontology.object_type import ObjectShape
from encord_active.common.iterator import Iterator
from encord_active.common.utils import get_bbox_from_encord_label_object
from encord_active.common.writer import CSVEmbeddingWriter
from PIL import Image
from torch import nn
from torchvision.models import EfficientNet_V2_S_Weights, efficientnet_v2_s
from torchvision.models.feature_extraction import create_feature_extractor

logger = logging.getLogger(__name__)
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def get_model_and_transforms() -> Tuple[nn.Module, nn.Module]:
    weights = EfficientNet_V2_S_Weights.DEFAULT
    model = efficientnet_v2_s(weights=weights).to(DEVICE)
    embedding_extractor = create_feature_extractor(model, return_nodes={"avgpool": "my_avgpool"})
    for p in embedding_extractor.parameters():
        p.requires_grad = False
    embedding_extractor.eval()
    return embedding_extractor, weights.transforms()


def adjust_image_channels(image: torch.Tensor) -> torch.Tensor:
    if image.shape[0] == 4:
        image = image[:3]
    elif image.shape[0] < 3:
        image = image.repeat(3, 1, 1)

    return image


def image_path_to_tensor(image_path: Path) -> torch.Tensor:
    image = Image.open(image_path.as_posix())
    transform = torch_transforms.ToTensor()
    image = transform(image)

    image = adjust_image_channels(image)

    return image


def assemble_object_batch(data_unit: dict, img_path: Path, transforms: Optional[nn.Module]):
    if transforms is None:
        transforms = torch.nn.Sequential()

    image = image_path_to_tensor(img_path)
    img_batch: List[torch.Tensor] = []
    for obj in data_unit["labels"]["objects"]:
        if obj["shape"] in [ObjectShape.POLYGON.value, ObjectShape.BOUNDING_BOX.value]:
            try:
                out = get_bbox_from_encord_label_object(
                    obj,
                    image.shape[2],
                    image.shape[1],
                )

                if out is None:
                    continue
                x, y, w, h = out

                img_patch = image[:, y : y + h, x : x + w]
                img_batch.append(transforms(img_patch))
            except Exception as e:
                logger.warning(f"Error with object {obj['objectHash']}: {e}")
                continue
    return torch.stack(img_batch).to(DEVICE) if len(img_batch) > 0 else None


@torch.inference_mode()
def generate_cnn_embeddings(iterator: Iterator, filename: str) -> None:
    start = time.perf_counter()
    feature_extractor, transforms = get_model_and_transforms()

    with CSVEmbeddingWriter(iterator.cache_dir, iterator, prefix=filename) as writer:
        for data_unit, img_pth in iterator.iterate(desc="Embedding data."):
            if img_pth is None:
                continue

            batches = assemble_object_batch(data_unit, img_pth, transforms=transforms)
            if batches is None:
                continue

            embeddings = feature_extractor(batches)["my_avgpool"]
            embeddings_torch = torch.flatten(embeddings, start_dim=1).cpu().detach().numpy()

            for obj, emb in zip(data_unit["labels"]["objects"], embeddings_torch):
                if obj["shape"] in [ObjectShape.POLYGON.value, ObjectShape.BOUNDING_BOX.value]:

                    last_edited_by = obj["lastEditedBy"] if "lastEditedBy" in obj.keys() else obj["createdBy"]

                    entry = {
                        "label_row": iterator.label_hash,
                        "data_unit": data_unit["data_hash"],
                        "frame": iterator.frame,
                        "objectHash": obj["objectHash"],
                        "lastEditedBy": last_edited_by,
                        "featureHash": obj["featureHash"],
                        "dataset_title": iterator.dataset_title,
                    }

                    writer.write_embedding(objects=obj, value=emb.tolist(), description=str(entry))

        logger.info(
            f"Generating {len(iterator)} embeddings took {str(time.perf_counter() - start)} seconds",
        )


@torch.inference_mode()
def generate_cnn_classification_embeddings(iterator: Iterator, filename: str) -> None:
    feature_node_hash_to_index: dict[str, dict] = {}

    # TODO_l This only evaluates immediate classes, not inherited ones
    for class_label in iterator.project.ontology["classifications"]:
        if class_label["attributes"][0]["type"] == ClassificationType.RADIO.value:
            feature_node_hash_to_index[class_label["featureNodeHash"]] = {}
            counter = 0
            for option in class_label["attributes"][0]["options"]:
                feature_node_hash_to_index[class_label["featureNodeHash"]][option["featureNodeHash"]] = counter
                counter += 1

    start = time.perf_counter()
    feature_extractor, transforms = get_model_and_transforms()

    with CSVEmbeddingWriter(iterator.cache_dir, iterator, prefix=filename) as writer:
        for data_unit, img_pth in iterator.iterate(desc="Embedding data."):
            if not img_pth:
                continue
            temp_entry = {}
            temp_entry["label_row"] = iterator.label_hash
            temp_entry["data_unit"] = data_unit["data_hash"]
            temp_entry["frame"] = data_unit["data_sequence"]
            temp_entry["url"] = data_unit["data_link"]

            temp_classification_hash = {}
            for classification in data_unit["labels"]["classifications"]:

                classification_hash = classification["classificationHash"]
                question_feature_hash = classification["featureHash"]
                if question_feature_hash in feature_node_hash_to_index:
                    for classification_answer in iterator.label_rows[iterator.label_hash]["classification_answers"][
                        classification_hash
                    ]["classifications"]:

                        if (
                            classification_answer["answers"][0]["featureHash"]
                            in feature_node_hash_to_index[question_feature_hash]
                        ):
                            temp_classification_hash[question_feature_hash] = {
                                "answer_featureHash": classification_answer["answers"][0]["featureHash"],
                                "answer_name": classification_answer["answers"][0]["name"],
                                "annotator": classification["createdBy"],
                            }

            temp_entry["classification_answers"] = temp_classification_hash  # type: ignore[assignment]

            image = image_path_to_tensor(img_pth)

            transformed_image = transforms(image).unsqueeze(0)

            embedding = feature_extractor(transformed_image.to(DEVICE))["my_avgpool"]
            embedding = torch.flatten(embedding).cpu().detach().numpy()

            writer.write_embedding(key=iterator.get_identifier(), value=embedding.tolist(), description=str(temp_entry))

        logger.info(
            f"Generating {len(iterator)} embeddings took {str(time.perf_counter() - start)} seconds",
        )


def get_cnn_embeddings(iterator: Iterator, embedding_type: str = "objects", *, force: bool = False) -> pd.DataFrame:
    target_folder = os.path.join(iterator.cache_dir, "embeddings")
    if embedding_type == "objects":
        embedding_file = "cnn_objects"
    elif embedding_type == "classifications":
        embedding_file = "cnn_classifications"
    else:
        raise Exception(f"Undefined embedding type '{embedding_type}' for get_cnn_embeddings method")

    embedding_path = os.path.join(target_folder, f"{embedding_file}.csv")

    if force:
        logger.info("Regenerating CNN embeddings...")
        if embedding_type == "objects":
            generate_cnn_embeddings(iterator, filename=embedding_file)
        elif embedding_type == "classifications":
            generate_cnn_classification_embeddings(iterator, filename=embedding_file)

        cnn_moments_df = pd.read_csv(embedding_path)
        logger.info("Done!")
    else:
        try:
            cnn_moments_df = pd.read_csv(embedding_path)
        except FileNotFoundError:
            logger.info(f"{embedding_path} not found. Generating embeddings...")
            if embedding_type == "objects":
                generate_cnn_embeddings(iterator, filename=embedding_file)
            elif embedding_type == "classifications":
                generate_cnn_classification_embeddings(iterator, filename=embedding_file)
            cnn_moments_df = pd.read_csv(embedding_path)
            logger.info("Done!")

    cnn_moments_df = cnn_moments_df.sort_values(["identifier"], ascending=True).reset_index()
    return cnn_moments_df
