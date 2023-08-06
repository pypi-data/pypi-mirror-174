from encord_active.common.indexer import AnnotationType, DataType, Indexer, IndexType
from encord_active.common.iterator import Iterator
from encord_active.common.writer import CSVIndexWriter


class ObjectsCountIndexer(Indexer):
    TITLE = "Object Count"
    SHORT_DESCRIPTION = "Counts number of objects in the image"
    LONG_DESCRIPTION = r"""Counts number of objects in the image."""
    INDEX_TYPE = IndexType.HEURISTIC
    DATA_TYPE = DataType.IMAGE
    ANNOTATION_TYPE = AnnotationType.ALL

    def test(self, iterator: Iterator, writer: CSVIndexWriter):
        for data_unit, img_pth in iterator.iterate(desc="Counting objects"):
            score = len(data_unit["labels"]["objects"])
            writer.write_score(score=score)
