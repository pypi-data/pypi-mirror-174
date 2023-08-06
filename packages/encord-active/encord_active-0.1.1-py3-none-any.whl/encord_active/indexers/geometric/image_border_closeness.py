from encord_active.common.indexer import AnnotationType, DataType, Indexer, IndexType
from encord_active.common.iterator import Iterator
from encord_active.common.utils import get_object_coordinates
from encord_active.common.writer import CSVIndexWriter
from loguru import logger

logger = logger.opt(colors=True)


class ImageBorderCloseness(Indexer):
    TITLE = "Annotation closeness to image borders"
    SHORT_DESCRIPTION = "Ranks annotations by how close they are to image borders."
    LONG_DESCRIPTION = r"""This indexer ranks annotations by how close they are to image borders."""
    INDEX_TYPE = IndexType.GEOMETRIC
    DATA_TYPE = DataType.IMAGE
    ANNOTATION_TYPE = [
        AnnotationType.OBJECT.BOUNDING_BOX,
        AnnotationType.OBJECT.POLYGON,
        AnnotationType.OBJECT.POLYLINE,
        AnnotationType.OBJECT.KEY_POINT,
        AnnotationType.OBJECT.SKELETON,
    ]

    def test(self, iterator: Iterator, writer: CSVIndexWriter):
        valid_annotation_types = {annotation_type.value for annotation_type in self.ANNOTATION_TYPE}
        found_any = False

        for data_unit, _ in iterator.iterate(desc="Computing closeness to border"):
            for obj in data_unit["labels"]["objects"]:
                if obj["shape"] not in valid_annotation_types:
                    continue

                coordinates = get_object_coordinates(obj)
                if not coordinates:  # avoid corrupted objects without vertices ([]) and unknown objects' shape (None)
                    continue

                x_coordinates = [x for x, _ in coordinates]
                min_x = min(x_coordinates)
                max_x = max(x_coordinates)

                y_coordinates = [y for _, y in coordinates]
                min_y = min(y_coordinates)
                max_y = max(y_coordinates)

                score = max(1 - min_x, 1 - min_y, max_x, max_y)
                writer.write_score(objects=obj, score=score)
                found_any = True

        if not found_any:
            logger.info(
                f"<yellow>[Skipping]</yellow> No object labels of types {{{', '.join(valid_annotation_types)}}}."
            )
