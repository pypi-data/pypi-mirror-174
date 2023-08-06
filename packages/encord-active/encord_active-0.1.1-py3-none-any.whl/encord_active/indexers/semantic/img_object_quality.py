import logging
from collections import Counter
from typing import List

import faiss
import numpy as np
import pandas as pd
from encord_active.common.indexer import (
    AnnotationType,
    DataType,
    EmbeddingType,
    Indexer,
    IndexType,
)
from encord_active.common.iterator import Iterator
from encord_active.common.utils import fix_duplicate_image_orders_in_knn_graph
from encord_active.common.writer import CSVIndexWriter
from encord_active.embeddings.cnn_embed import get_cnn_embeddings
from tqdm import tqdm

logger = logging.getLogger(__name__)


class ObjectEmbeddingSimilarityTest(Indexer):
    TITLE = "Object Annotation Quality"
    SHORT_DESCRIPTION = "Compares object annotations against similar image crops"
    LONG_DESCRIPTION = r"""This indexer transforms polygons into bounding boxes 
    and an embedding for each bounding box is extracted. Then, these embeddings are compared
    with their neighbors. If the neighbors are annotated differently, a low score is given to it.
    """
    NEEDS_IMAGES = True
    EMBEDDING_TYPE = EmbeddingType.OBJECT
    INDEX_TYPE = IndexType.SEMANTIC
    DATA_TYPE = DataType.IMAGE
    ANNOTATION_TYPE = [AnnotationType.OBJECT.BOUNDING_BOX, AnnotationType.OBJECT.POLYGON]

    def __init__(self, num_nearest_neighbors: int = 10, certainty_ratio: float = 0.6, project_dataset_name: str = ""):
        """
        :param num_nearest_neighbors: determines how many nearest neighbors' labels should be checked for the quality.
         This parameter should be +1 than the actual intended number because in the nearest neighbor graph queried
         embedding already exists
        :param project_dataset_name: if QM is wanted to be run on specific dataset, name should be given here. If it is
         empty, it means evaluate all datasets in the project
        """
        super(ObjectEmbeddingSimilarityTest, self).__init__()
        self.collections: dict[str, dict] = {}
        self.featureNodeHash_to_index: dict[str, int] = {}
        self.index_to_object_name: dict[int, str] = {}
        self.object_name_to_index: dict[str, int] = {}
        self.num_nearest_neighbors = num_nearest_neighbors
        self.certainty_ratio = certainty_ratio
        self.project_dataset_name = project_dataset_name

    def setup(self, iterator) -> bool:
        found_any = False
        for i, object_label in enumerate(iterator.project.ontology["objects"]):
            found_any = True
            self.featureNodeHash_to_index[object_label["featureNodeHash"]] = i
            self.index_to_object_name[i] = object_label["name"]
            self.object_name_to_index[object_label["name"]] = i
        return found_any

    def convert_to_index(self):
        embeddings_list: List[list] = []
        noisy_labels_list: List[int] = []
        for x in self.collections.values():
            embeddings_list.append(x["embedding"])
            noisy_labels_list.append(self.object_name_to_index[x["name"]])

        embeddings = np.array(embeddings_list).astype(np.float32)
        noisy_labels = np.array(noisy_labels_list).astype(np.int32)

        db_index = faiss.IndexFlatL2(embeddings.shape[1])
        db_index.add(embeddings)  # pylint: disable=no-value-for-parameter
        return embeddings, db_index, noisy_labels

    def get_description_info(self, nearest_labels: np.ndarray, noisy_label: int):
        threshold = int(len(nearest_labels) * self.certainty_ratio)
        counter = Counter(nearest_labels)
        target_label, target_label_frequency = counter.most_common(1)[0]

        if noisy_label == target_label and target_label_frequency > threshold:
            description = (
                f":heavy_check_mark: The object is correctly annotated as `{self.index_to_object_name[noisy_label]}`"
            )
        elif noisy_label != target_label and target_label_frequency > threshold:
            description = f":x: The object is annotated as `{self.index_to_object_name[noisy_label]}`. Similar \
             objects were annotated as `{self.index_to_object_name[target_label]}`."
        else:  # covers cases for  target_label_frequency <= threshold:
            description = f":question: The object is annotated as `{self.index_to_object_name[noisy_label]}`. \
            The annotated class may be wrong, as the most similar objects have different classes."
        return description

    def unpack_collections(self, embeddings_df: pd.DataFrame) -> None:
        for item in tqdm(embeddings_df.itertuples(), desc="Unpacking embeddings"):
            tmp_entry = eval(item.description)
            if tmp_entry["dataset_title"] == self.project_dataset_name or self.project_dataset_name == "":
                tmp_entry["embedding"] = np.array(
                    [float(x) for x in item.embedding[1:-1].replace(" ", "").split(",")],
                    dtype=np.float32,
                )
                tmp_entry["name"] = item.object_class
                self.collections[item.identifier] = tmp_entry

    def test(self, iterator: Iterator, writer: CSVIndexWriter):
        ontology_contains_objects = self.setup(iterator)
        if not ontology_contains_objects:
            logger.info("<yellow>[Skipping]</yellow> No objects in the project ontology.")
            return

        cnn_embeddings_df = get_cnn_embeddings(iterator, embedding_type="objects")
        if cnn_embeddings_df.shape[0] > 0:
            embedding_identifiers = cnn_embeddings_df.identifier.values.tolist()

            self.unpack_collections(cnn_embeddings_df)

            embedding_database, index, noisy_labels = self.convert_to_index()
            nearest_distances, nearest_indexes = index.search(  # pylint: disable=no-value-for-parameter
                embedding_database, self.num_nearest_neighbors
            )
            nearest_indexes = fix_duplicate_image_orders_in_knn_graph(nearest_indexes)

            nearest_labels = np.take(noisy_labels, nearest_indexes)
            noisy_labels_tmp, nearest_labels_except_self = np.split(nearest_labels, [1], axis=-1)
            assert np.all(noisy_labels == noisy_labels_tmp.squeeze()), "Failed class index extraction"

            label_matches = np.equal(nearest_labels_except_self, np.expand_dims(noisy_labels, axis=-1))
            collections_scores = label_matches.mean(axis=-1)

            valid_annotation_types = {annotation_type.value for annotation_type in self.ANNOTATION_TYPE}
            for data_unit, img_pth in iterator.iterate(desc="Storing index"):
                for obj in data_unit["labels"]["objects"]:
                    if obj["shape"] not in valid_annotation_types:
                        continue

                    key = iterator.get_identifier(object=obj)
                    # This index indicate the position in the embedding df of the current iterator object
                    try:
                        idx = embedding_identifiers.index(key)
                    except ValueError:
                        logger.warning(f"{key} not found in embeddings df")
                        continue

                    assert (
                        obj["name"] == self.collections[key]["name"] == cnn_embeddings_df.iloc[idx].object_class
                    ), "Indexing inconsistencies"

                    writer.write_score(
                        objects=obj,
                        score=collections_scores[idx],
                        description=self.get_description_info(nearest_labels_except_self[idx], noisy_labels[idx]),
                    )
        else:
            logger.info("<yellow>[Skipping]</yellow> The object embedding file is empty.")
