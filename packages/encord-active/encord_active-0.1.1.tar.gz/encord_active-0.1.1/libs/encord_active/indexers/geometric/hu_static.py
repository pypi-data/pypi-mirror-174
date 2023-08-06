from typing import List

import numpy as np
from encord_active.common.indexer import AnnotationType, DataType, Indexer, IndexType
from encord_active.common.iterator import Iterator
from encord_active.common.utils import get_object_coordinates
from encord_active.common.writer import CSVEmbeddingWriter, CSVIndexWriter
from encord_active.embeddings.hu_embed import get_hu_embeddings
from loguru import logger
from sklearn.decomposition import PCA

logger = logger.opt(colors=True)


def compute_cls_distances(embeddings: np.ndarray, labels: np.ndarray) -> np.ndarray:
    """Compute distance between class samples and the class centroid."""
    cls_distance_vector = np.zeros_like(labels, dtype=np.float32)
    for cls in set(labels):
        cls_mask = labels == cls
        cls_embeddings = embeddings[cls_mask]
        centroid = cls_embeddings.mean(axis=0)
        cls_distances = np.linalg.norm(cls_embeddings - centroid, axis=1)
        cls_distance_vector[cls_mask] = cls_distances
    cls_distance_vector[cls_distance_vector == 0] = cls_distance_vector[cls_distance_vector != 0].min()
    return cls_distance_vector


class HuMomentsStatic(Indexer):
    TITLE = "Shape outlier detection"
    SHORT_DESCRIPTION = "Calculates potential outliers by polygon shape."
    LONG_DESCRIPTION = r"""Computes the Euclidean distance between the polygons' 
    [Hu moments](https://en.wikipedia.org/wiki/Image_moment) for each class and 
    the prototypical class moments."""
    SCORE_NORMALIZATION = True
    INDEX_TYPE = IndexType.GEOMETRIC
    DATA_TYPE = DataType.IMAGE
    ANNOTATION_TYPE = [AnnotationType.OBJECT.POLYGON]

    def test(self, iterator: Iterator, writer: CSVIndexWriter):
        valid_annotation_types = {annotation_type.value for annotation_type in self.ANNOTATION_TYPE}
        hu_moments_df = get_hu_embeddings(iterator, force=True)

        moments_list: List[np.ndarray] = []
        obj_list: List[dict] = []
        obj_hashes: List[str] = []
        cls_list: List[str] = []
        for data_unit, img_pth in iterator.iterate(desc="Computing HU moments"):
            for obj in data_unit["labels"]["objects"]:
                if obj["shape"] not in valid_annotation_types:
                    continue

                points = get_object_coordinates(obj)
                if not points:  # avoid corrupted objects without vertices ([])
                    continue

                key = writer.get_identifier(obj)
                moments = np.array(eval(hu_moments_df.loc[hu_moments_df["identifier"] == key, "embedding"].values[0]))

                obj_list.append(obj)
                obj_hashes.append(obj["objectHash"])
                cls_list.append(obj["name"])
                moments_list.append(moments)

        cls_dict = {cls: i for i, cls in enumerate(set(cls_list))}
        cls_ary = np.array([cls_dict[cls] for cls in cls_list])

        if not moments_list:
            logger.info("<yellow>[Skipping]</yellow> No polygons to evaluate.")
            return

        X = np.stack(moments_list, axis=0)
        X = (X - X.mean(0)) / X.std(0)

        distance_vector = 1 / compute_cls_distances(X, cls_ary)
        n = len(obj_list)
        for data_unit, img_pth in iterator.iterate(desc="writing scores"):
            for obj in data_unit["labels"]["objects"]:
                try:
                    index = obj_hashes.index(obj["objectHash"])
                except:
                    continue

                writer.write_score(objects=obj, score=float(distance_vector[index]), object_class=cls_list[index])

        pca_coordinates = PCA(n_components=2).fit_transform(X)
        with CSVEmbeddingWriter(iterator.cache_dir, iterator, prefix="hu_2d-embedding") as coords_writer:
            for data_unit, img_pth in iterator.iterate(desc="writing scores"):
                for obj in data_unit["labels"]["objects"]:
                    try:
                        index = obj_hashes.index(obj["objectHash"])
                    except:
                        continue

                    coords_writer.write_embedding(
                        objects=obj, value=pca_coordinates[index].tolist(), object_class=cls_list[index]
                    )
