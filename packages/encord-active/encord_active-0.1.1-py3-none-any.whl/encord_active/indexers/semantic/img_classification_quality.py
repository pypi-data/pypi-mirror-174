import os
import pickle
from collections import Counter
from pathlib import Path

import faiss
import numpy as np
import pandas as pd
import torch
from encord_active.common.indexer import (
    AnnotationType,
    DataType,
    EmbeddingType,
    Indexer,
    IndexType,
)
from encord_active.common.iterator import Iterator
from encord_active.common.writer import CSVIndexWriter
from encord_active.embeddings.cnn_embed import get_cnn_embeddings
from loguru import logger
from tqdm import tqdm

logger = logger.opt(colors=True)
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")


class ImageLevelQualityTest(Indexer):
    TITLE = "Image-level Annotation Quality"
    SHORT_DESCRIPTION = "Compares image classifications against similar images"
    LONG_DESCRIPTION = r"""This index creates embeddings from images. Then, these embeddings are used to build
    nearest neighbor graph. Similar embeddings' classifications are compared against each other.
        """
    NEEDS_IMAGES = True
    EMBEDDING_TYPE = EmbeddingType.CLASSIFICATION
    INDEX_TYPE = IndexType.SEMANTIC
    DATA_TYPE = DataType.IMAGE
    ANNOTATION_TYPE = [AnnotationType.CLASSIFICATION.RADIO]

    def __init__(self, num_nearest_neighbors: int = 10, certainty_ratio: float = 0.60):
        """

        :param num_nearest_neighbors: determines how many nearest neighbors' labels should be checked for the quality.
        This parameter should be +1 than the actual intended number because in the nearest neighbor graph queried
        embedding already exists
        :param certainty_ratio: ratio to determine if the annotation is mislabeled or there is a different problem in
        the annotation
        """
        super(ImageLevelQualityTest, self).__init__()
        self.collections: list[dict] = []
        self.featureNodeHash_to_index: dict[str, dict] = {}
        self.featureNodeHash_to_name: dict[str, dict] = {}
        self.featureNodeHash_to_question_name: dict[str, str] = {}
        self.index_to_answer_name: dict[str, dict] = {}
        self.identifier_to_embedding: dict[str, np.ndarray] = {}
        self.question_hash_to_collection_indexes: dict[str, list] = {}
        self.cache_dir: Path = Path()
        self.num_nearest_neighbors = num_nearest_neighbors
        self.certainty_ratio = certainty_ratio

    def extract_description_info(self, question_hash: str, nearest_labels: dict[str, np.ndarray], index: int):
        gt_label = nearest_labels["gt_label"][index]
        neighbor_labels = nearest_labels["neighbor_labels"][index].tolist()

        threshold = int(len(neighbor_labels) * self.certainty_ratio)
        counter = Counter(neighbor_labels)
        target_label, target_label_frequency = counter.most_common(1)[0]

        if gt_label == target_label and target_label_frequency > threshold:
            description = f":heavy_check_mark: For the question `{self.featureNodeHash_to_question_name[question_hash]}`, the image is correctly annotated as `{self.index_to_answer_name[question_hash][gt_label]}`"

        elif gt_label != target_label and target_label_frequency > threshold:
            description = f":x: For the question `{self.featureNodeHash_to_question_name[question_hash]}`, the image is annotated as `{self.index_to_answer_name[question_hash][gt_label]}`. Similar \
             images were annotated as `{self.index_to_answer_name[question_hash][target_label]}`."

        else:  # covers cases for  target_label_frequency <= threshold:
            description = f":question: For the question `{self.featureNodeHash_to_question_name[question_hash]}`, the image is annotated as `{self.index_to_answer_name[question_hash][gt_label]}`. \
            The annotated class may be wrong, as the most similar objects have different classes."

        return description

    def convert_to_indexes(self):
        embedding_databases, indexes = {}, {}

        for question_hash in self.featureNodeHash_to_name.keys():
            selected_collections = [
                self.collections[i] for i in self.question_hash_to_collection_indexes[question_hash]
            ]
            if len(selected_collections) > self.num_nearest_neighbors:
                embedding_database = np.stack(list(map(lambda x: x["embedding"], selected_collections)))

                index = faiss.IndexFlatL2(embedding_database.shape[1])
                index.add(embedding_database)  # pylint: disable=no-value-for-parameter

                embedding_databases[question_hash] = embedding_database
                indexes[question_hash] = index

        return embedding_databases, indexes

    def get_nearest_indexes(self):
        # from collections build faiss index
        embedding_databases, indexes = self.convert_to_indexes()

        nearest_indexes = {}
        for question_hash in indexes:
            # TODO Check proper usage of index.search()
            nearest_distance, nearest_index = indexes[question_hash].search(  # pylint: disable=no-value-for-parameter
                embedding_databases[question_hash], self.num_nearest_neighbors
            )
            nearest_indexes[question_hash] = nearest_index

        return nearest_indexes

    def transform_neighbors_to_labels_for_all_questions(self, nearest_indexes: dict[str, np.ndarray]):
        nearest_labels_all_questions = {}

        for question in nearest_indexes:
            noisy_labels_list = []
            for i in range(nearest_indexes[question].shape[0]):
                collection_index = self.question_hash_to_collection_indexes[question][i]
                answer_featureHash = self.collections[collection_index]["classification_answers"][question][
                    "answer_featureHash"
                ]
                gt_label = self.featureNodeHash_to_index[question][answer_featureHash]
                noisy_labels_list.append(gt_label)

            noisy_labels = np.array(noisy_labels_list).astype(np.int32)
            nearest_labels = np.take(noisy_labels, nearest_indexes[question])
            noisy_labels_tmp, nearest_labels_except_self = np.split(nearest_labels, [1], axis=-1)
            assert np.all(noisy_labels == noisy_labels_tmp.squeeze()), "Failed class index extraction"

            nearest_labels_all_questions[question] = {
                "gt_label": noisy_labels,
                "neighbor_labels": nearest_labels_except_self,
            }

        return nearest_labels_all_questions

    def convert_nearest_labels_to_scores(self, nearest_labels: dict[str, np.ndarray]) -> list[float]:
        """
        Higher scores mean more reliable label
        :param nearest_labels: output of the index.search()
        :return: score for each row
        """

        label_matches = np.equal(nearest_labels["neighbor_labels"], np.expand_dims(nearest_labels["gt_label"], axis=-1))
        collections_scores = label_matches.mean(axis=-1)

        return collections_scores

    def convert_nearest_labels_to_scores_for_all_questions(self, nearest_labels_all_questions: dict[str, dict]):
        collections_scores_all_questions = {}
        for question in nearest_labels_all_questions:
            scores = self.convert_nearest_labels_to_scores(nearest_labels_all_questions[question])
            collections_scores_all_questions[question] = scores
        return collections_scores_all_questions

    def create_key_score_pairs(self, nearest_indexes: dict[str, np.ndarray]) -> dict[str, dict]:

        nearest_labels_all_questions = self.transform_neighbors_to_labels_for_all_questions(nearest_indexes)
        collections_scores_all_questions = self.convert_nearest_labels_to_scores_for_all_questions(
            nearest_labels_all_questions
        )

        key_score_pairs = {}
        for i, collection in enumerate(self.collections):
            label_hash = collection["label_row"]
            du_hash = collection["data_unit"]
            frame_idx = int(collection["frame"])

            key = f"{label_hash}_{du_hash}_{frame_idx:05d}"

            temp_entry = {}
            for question in collection["classification_answers"]:
                sub_collection_index = self.question_hash_to_collection_indexes[question].index(i)
                score = collections_scores_all_questions[question][sub_collection_index]

                temp_entry[question] = {
                    "score": score,
                    "description": self.extract_description_info(
                        question, nearest_labels_all_questions[question], sub_collection_index
                    ),
                    "class_name": self.featureNodeHash_to_question_name[question],
                    "annotator": collection["classification_answers"][question]["annotator"],
                }

            key_score_pairs[key] = temp_entry
        return key_score_pairs

    def build_question_hash_to_collection_index(self):
        target_folder = os.path.join(self.cache_dir, "embeddings")
        embedding_metadata_path = os.path.join(target_folder, "embedding_classifications_metadata.pkl")
        if os.path.isfile(embedding_metadata_path):
            with open(embedding_metadata_path, "rb") as f:
                self.question_hash_to_collection_indexes = pickle.load(f)
        else:
            for question_hash in self.featureNodeHash_to_name.keys():
                self.question_hash_to_collection_indexes[question_hash] = []

            for i, collection in enumerate(self.collections):
                for question_hash in self.featureNodeHash_to_name.keys():
                    if question_hash in collection["classification_answers"]:
                        self.question_hash_to_collection_indexes[question_hash].append(i)

            if not os.path.isdir(target_folder):
                os.makedirs(target_folder)
            with open(embedding_metadata_path, "wb") as f:
                pickle.dump(self.question_hash_to_collection_indexes, f)

    def fix_nearest_indexes(self, nearest_indexes: dict[str, np.ndarray]) -> None:
        """
        In the presence of duplicate images, ordering of the nearest indexes might be confused. This function ensures
        that first column value is always equal to row number.
        :param nearest_indexes: dictionary to keep the nearest indexes for different classification questions
        :return: None
        """
        for question in nearest_indexes:
            question_nearest_indexes = nearest_indexes[question]
            for i in range(question_nearest_indexes.shape[0]):
                if i != question_nearest_indexes[i, 0]:
                    item_index = np.where(question_nearest_indexes[i] == i)[0][0]
                    question_nearest_indexes[i, 0], question_nearest_indexes[i, item_index] = (
                        question_nearest_indexes[i, item_index],
                        question_nearest_indexes[i, 0],
                    )

    def setup(self, iterator: Iterator) -> bool:
        """
        Looks for classes to use.
        :param iterator:
        :return: True if there is anything to do based on the ontology. Otherwise False.
        """
        self.cache_dir = iterator.cache_dir
        # TODO_l This only evaluates immediate classes, not inherited ones
        found_any = False
        for class_label in iterator.project.ontology["classifications"]:
            if "options" in class_label["attributes"][0]:
                found_any = True
                self.featureNodeHash_to_index[class_label["featureNodeHash"]] = {}
                self.featureNodeHash_to_name[class_label["featureNodeHash"]] = {}
                self.featureNodeHash_to_question_name[class_label["featureNodeHash"]] = class_label["attributes"][0][
                    "name"
                ]
                self.index_to_answer_name[class_label["featureNodeHash"]] = {}
                counter = 0
                for option in class_label["attributes"][0]["options"]:
                    self.featureNodeHash_to_index[class_label["featureNodeHash"]][option["featureNodeHash"]] = counter
                    self.featureNodeHash_to_name[class_label["featureNodeHash"]][option["featureNodeHash"]] = option[
                        "label"
                    ]
                    self.index_to_answer_name[class_label["featureNodeHash"]][counter] = option["label"]

                    counter += 1
        return found_any

    def unpack_collections(self, embeddings_df: pd.DataFrame) -> None:
        for item in tqdm(embeddings_df.itertuples(), desc="Unpacking embeddings"):
            tmp_entry = eval(item.description)
            tmp_entry["embedding"] = np.array(
                [float(x) for x in item.embedding[1:-1].replace(" ", "").split(",")],
                dtype=np.float32,
            )
            self.collections.append(tmp_entry)

    def test(self, iterator: Iterator, writer: CSVIndexWriter):
        project_has_classifications = self.setup(iterator)
        if not project_has_classifications:
            logger.info("<yellow>[Skipping]</yellow> No frame level classifications in the project ontology.")

        cnn_embeddings_df = get_cnn_embeddings(iterator, embedding_type="classifications")
        if cnn_embeddings_df.shape[0] > 0:
            self.unpack_collections(cnn_embeddings_df)

            self.build_question_hash_to_collection_index()
            nearest_indexes = self.get_nearest_indexes()
            self.fix_nearest_indexes(nearest_indexes)
            key_score_pairs = self.create_key_score_pairs(nearest_indexes)

            for data_unit, img_pth in iterator.iterate(desc="Storing index"):
                key = iterator.get_identifier()
                if key in key_score_pairs:
                    for classification in data_unit["labels"]["classifications"]:
                        question_featureHash = classification["featureHash"]
                        if question_featureHash in key_score_pairs[key]:
                            writer.write_score(
                                key=key + "_" + question_featureHash,
                                value=key_score_pairs[key][question_featureHash]["score"],
                                description=key_score_pairs[key][question_featureHash]["description"],
                                objects=classification,
                            )
        else:
            logger.info("<yellow>[Skipping]</yellow> The embedding file is empty.")
