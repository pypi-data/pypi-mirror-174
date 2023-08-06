from abc import ABC, abstractmethod
from enum import Enum
from hashlib import md5
from typing import List, Optional, Union

from encord.project_ontology.classification_type import ClassificationType
from encord.project_ontology.object_type import ObjectShape
from encord_active.common.iterator import Iterator
from encord_active.common.writer import CSVIndexWriter


class IndexType(Enum):
    SEMANTIC = "semantic"
    GEOMETRIC = "geometric"
    HEURISTIC = "heuristic"


class DataType(Enum):
    IMAGE = "image"
    SEQUENCE = "sequence"


class AnnotationType:
    NONE = None
    OBJECT = ObjectShape
    CLASSIFICATION = ClassificationType
    ALL = [OBJECT, CLASSIFICATION]


class EmbeddingType(Enum):
    CLASSIFICATION = "classification"
    OBJECT = "object"
    HU_MOMENTS = "hu_moments"
    NONE = "none"


class Indexer(ABC):
    @abstractmethod
    def test(self, iterator: Iterator, writer: CSVIndexWriter):
        """
        This is where you should perform your data indexing.

        :param iterator: The iterator with which you can iterate through the dataset as
            many times you like. The iterator scans through one label rows at a time,
            continuously indexing each frame of a video.

            Use::

                for data_unit, img_pth in iterator.iterate(desc="Progress bar description"):
                    pass


        :param writer:  The writer to which you should store your scores.
            Use::

                writer.write_score(key, value, description)


        :return:
        """
        pass

    @property
    @abstractmethod
    def TITLE(self) -> str:
        """
        Set the title of your indexer. Aim for no more than 80 characters.
        The title will be used, e.g., when displaying results in the app.

        The property can, e.g., be set as a class property::

            class MyClass(Indexer):
                TITLE = "This is the title"
                # ...

        """
        pass

    @property
    @abstractmethod
    def INDEX_TYPE(self) -> IndexType:
        """
        Type of the indexer. Choose one of the following:
            - Geometric: indexers related to the geometric properties of annotations.
            This type includes size, shape, location, etc.
            - Semantic: indexers based on the *contents* of annotations, images or videos.
            This type includes ResNet embedding distances, image uncertainties, etc.
            - Heuristic: any other indexer. For example, brightness, sharpness, object counts, etc.


        The property can, e.g., be set as a class property::

            class MyClass(Indexer):
                INDEX_TYPE = IndexType.GEOMETRIC
                # ...

        """
        pass

    @property
    @abstractmethod
    def DATA_TYPE(self) -> Union[List[DataType], DataType]:
        """
        Type of data with which the indexer operates. Choose one of the following:
            - Image: indexer requires individual images. E.g. bounding box location
            - Sequence: indexer requires sequences of images to harness temporal information
                (videos, e.g. bounding box IoU across video frames) or volumetric information
                (DICOM, e.g. bounding box IoU across slices).

        The property can, e.g., be set as a class property::

            class MyClass(Indexer):
                DATA_TYPE = DataType.IMAGE
                # ...

        """
        pass

    @property
    @abstractmethod
    def ANNOTATION_TYPE(self) -> Optional[Union[List[AnnotationType], AnnotationType]]:
        """
        Type of annotations the indexer operates needs. Choose one of the following:
            - Object: includes bounding box, polygon, polyline, keypoint and skeleton
            - Classification: includes text, radio button and checklist

        The property can, e.g., be set as a class property::

            class MyClass(Indexer):
                ANNOTATION_TYPE = AnnotationType.OBJECT.POLYGON
                # ...

        """
        pass

    @property
    @abstractmethod
    def SHORT_DESCRIPTION(self) -> str:
        """
        Set a short description of what the indexer does. Aim for at most 120
        characters. As for the title, this can be set as a class property.

        The short description will be used in lists and other places, where space is
        limited.
        """
        pass

    @property
    @abstractmethod
    def LONG_DESCRIPTION(self) -> str:
        """
        Set a verbose description of what the indexer does. If it is based on ideas
        from papers, etc., this is where such links can be included. If you write
        markdown, this will be rendered appropriately in the app.

        The long description will be used when much space is available and when
        providing full details makes sense.
        """
        pass

    @property
    def SCORE_NORMALIZATION(self) -> bool:
        """
        If the score normalization will be applied to indices from this indexer as default in the app.
        :return: True or False
        """

        return False

    @property
    def NEEDS_IMAGES(self):
        """
        If the indexer need to look at image content. This is automatically inferred from the index type:
            - IndexType.GEOMETRIC: False
            - IndexType.SEMANTIC: True
            - IndexType.HEURISTIC: True

        """
        return False if self.INDEX_TYPE == IndexType.GEOMETRIC else True

    def get_unique_name(self):
        name_hash = md5((self.TITLE + self.SHORT_DESCRIPTION + self.LONG_DESCRIPTION).encode()).hexdigest()

        return f"{name_hash[:8]}_{self.TITLE.lower().replace(' ', '_')}"
