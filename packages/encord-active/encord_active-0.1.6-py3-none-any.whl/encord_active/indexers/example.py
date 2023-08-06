from encord_active.common.indexer import AnnotationType, DataType, Indexer, IndexType
from encord_active.common.iterator import Iterator
from encord_active.common.writer import CSVIndexWriter
from loguru import logger

logger = logger.opt(colors=True)


class ExampleIndexer(Indexer):
    TITLE = "Example Title"
    INDEX_TYPE = IndexType.HEURISTIC
    DATA_TYPE = DataType.IMAGE
    ANNOTATION_TYPE = [AnnotationType.OBJECT.BOUNDING_BOX, AnnotationType.OBJECT.POLYGON]
    SHORT_DESCRIPTION = "Assigns same value and description to all objects."
    LONG_DESCRIPTION = r"""For long descriptions, I can use Markdown to _format_ the text.  
    
I can, e.g., make a 
[hyperlink](https://memegenerator.net/instance/74454868/europe-its-the-final-markdown) 
to the awesome paper that proposed the method.

Or use math to better explain the method: 
$$h_{\lambda}(x) = \frac{1}{x^\intercal x}$$
"""

    def test(self, iterator: Iterator, writer: CSVIndexWriter):
        valid_annotation_types = {annotation_type.value for annotation_type in self.ANNOTATION_TYPE}

        logger.info("My custom logging")

        # Preprocessing happens here.
        # You can build/load databases of embeddings, compute statistics etc,
        # ...

        for data_unit, img_pth in iterator.iterate(desc="Progress bar description"):
            # Frame level score (data quality)
            writer.write_score(score=1337, description="Your description of the index score [can be omitted]")

            for obj in data_unit["labels"]["objects"]:
                # Object level score (label / model prediction quality)
                if not obj["shape"] in valid_annotation_types:
                    continue

                # This is where you do the actual inference.

                # Some convenient properties associated with the current data.
                # ``iterator.label_hash`` the label hash of the current data unit
                # ``iterator.du_hash`` the data unit hash of
                # ``iterator.frame`` the frame of the current data unit hash of
                # ``iterator.num_frames`` the total number of frames in the label row.

                # Do your thing (inference)
                # ...
                # Then
                writer.write_score(
                    objects=obj, score=42, description="Your description of the index score [can be omitted]"
                )
