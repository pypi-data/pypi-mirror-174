import csv
import math
from abc import ABC, abstractmethod
from itertools import chain
from pathlib import Path
from typing import List, Optional, Union

import numpy as np
from encord_active.common.iterator import Iterator

SCORE_CSV_FIELDS = ["identifier", "score", "description", "object_class", "annotator", "frame", "url"]
EMBEDDING_CSV_FIELDS = ["identifier", "embedding", "description", "object_class", "frame", "url"]


class IndexObserver(ABC):
    @abstractmethod
    def on_value_insert(self, value: Union[float, int, list]):
        pass

    @abstractmethod
    def on_index_close(self):
        pass


class StatisticsObserver(IndexObserver):
    def __init__(self):
        self.min_value = math.inf
        self.max_value = -math.inf
        self.num_rows = 0
        self.mean_value = 0

    def on_value_insert(self, value: Union[float, int, list]):
        if isinstance(value, list):
            value = float(np.linalg.norm(np.array(value)))
        elif not isinstance(value, (int, float)):
            raise TypeError(f"Expected float, int, or list, got {type(value)}")

        self.min_value = min(self.min_value, value)
        self.max_value = max(self.max_value, value)
        self.mean_value = (self.mean_value * self.num_rows + value) / (self.num_rows + 1)
        self.num_rows += 1

    def on_index_close(self):
        pass


class Writer(ABC):
    _observers: List[IndexObserver] = []

    def attach(self, observer: IndexObserver):
        self._observers.append(observer)

    def remove_listener(self, observer: IndexObserver):
        self._observers.remove(observer)

    @abstractmethod
    def __enter__(self):
        pass

    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb):
        for observer in self._observers:
            observer.on_index_close()

    def write_value(self, value: Union[float, int, list]):
        for observer in self._observers:
            observer.on_value_insert(value)


class CSVWriter(Writer):
    def __init__(self, filename: Path, iterator: Iterator):
        super(CSVWriter, self).__init__()

        self.iterator = iterator

        self.filename = filename
        self.filename.parent.mkdir(parents=True, exist_ok=True)
        self.csv_file = self.filename.open("w", newline="", encoding="utf-8")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.csv_file.close()  # Notify observers
        super(CSVWriter, self).__exit__(exc_type, exc_val, exc_tb)

    def get_identifier(
        self,
        objects: Union[list[dict], dict, None] = None,
        label_hash: Optional[str] = None,
        du_hash: Optional[str] = None,
        frame: Optional[int] = None,
    ):
        label_hash = self.iterator.label_hash if label_hash is None else label_hash
        du_hash = self.iterator.du_hash if du_hash is None else du_hash
        frame = self.iterator.frame if frame is None else frame

        key = f"{label_hash}_{du_hash}_{frame:05d}"

        if objects is not None:
            if isinstance(objects, dict):
                objects = [objects]
            hashes = [obj["objectHash"] if "objectHash" in obj else obj["classificationHash"] for obj in objects]
            return "_".join(chain([key], hashes))
        return key


class CSVIndexWriter(CSVWriter):
    def __init__(self, data_path: Path, iterator: Iterator, prefix: str):
        filename = (data_path / "indexes" / f"{prefix}.csv").expanduser()
        super(CSVIndexWriter, self).__init__(filename=filename, iterator=iterator)

        self.writer = csv.DictWriter(self.csv_file, fieldnames=SCORE_CSV_FIELDS)
        self.writer.writeheader()

    def write_score(
        self,
        key: Optional[str] = None,
        value: Union[float, int, None] = None,
        description: str = "",
        object_class: Optional[str] = None,
        label_hash: Optional[str] = None,
        du_hash: Optional[str] = None,
        frame: Optional[int] = None,
        url: Optional[str] = None,
        annotator: Optional[str] = None,
        objects: Union[list[dict], dict, None] = None,
        score: Union[float, int, None] = None,
    ):
        # TODO erase hack sections when CSVIndexWriter's format (obj, score) is enforced on all indexers
        # maintain hack code sections while format (obj, score) progress across indexers replacing (key, value)

        # while variable 'value' is used by an indexer its value must be transferred to score
        # start hack
        score = value if score is None else score
        # end hack

        if not isinstance(score, (float, int)):
            raise TypeError("Score must be a float or int")
        if isinstance(objects, list) and len(objects) == 0:
            objects = None
        elif isinstance(objects, dict):
            objects = [objects]

        label_hash = self.iterator.label_hash if label_hash is None else label_hash
        du_hash = self.iterator.du_hash if du_hash is None else du_hash
        frame = self.iterator.frame if frame is None else frame
        url = self.iterator.get_data_url() if url is None else url

        if objects is None:
            object_class = "" if object_class is None else object_class
            annotator = "" if annotator is None else annotator
        else:
            object_class = objects[0]["name"] if object_class is None else object_class
            annotator = objects[0]["lastEditedBy"] if "lastEditedBy" in objects[0] else objects[0]["createdBy"]

        # remember to remove if clause (not its content) when writer's format (obj, score) is enforced on all indexers
        # start hack
        if key is None:
            key = self.get_identifier(objects, label_hash, du_hash, frame)
        # end hack

        row = {
            "identifier": key,
            "score": score,
            "description": description,
            "object_class": object_class,
            "frame": frame,
            "url": url,
            "annotator": annotator,
        }

        self.writer.writerow(row)
        self.csv_file.flush()

        super(CSVIndexWriter, self).write_value(score)


class CSVEmbeddingWriter(CSVWriter):
    def __init__(self, data_path: Path, iterator: Iterator, prefix: str):
        filename = (data_path / "embeddings" / f"{prefix}.csv").expanduser()
        super(CSVEmbeddingWriter, self).__init__(filename=filename, iterator=iterator)

        self.writer = csv.DictWriter(self.csv_file, fieldnames=EMBEDDING_CSV_FIELDS)
        self.writer.writeheader()

    def write_embedding(
        self,
        key: Optional[str] = None,
        value: Union[float, list, None] = None,
        description: str = "",
        object_class: Optional[str] = None,
        label_hash: Optional[str] = None,
        du_hash: Optional[str] = None,
        frame: Optional[int] = None,
        url: Optional[str] = None,
        objects: Union[list[dict], dict, None] = None,
    ):
        # TODO remove value parameter as optional when objects parameters is enforced as first parameter instead of keys
        if not isinstance(value, (float, list)):
            raise TypeError("value must be a float or list")

        if isinstance(objects, list) and len(objects) == 0:
            objects = None
        elif isinstance(objects, dict):
            objects = [objects]

        label_hash = self.iterator.label_hash if label_hash is None else label_hash
        du_hash = self.iterator.du_hash if du_hash is None else du_hash
        frame = self.iterator.frame if frame is None else frame
        url = self.iterator.get_data_url() if url is None else url

        if objects is None:
            object_class = "" if object_class is None else object_class
        else:
            object_class = objects[0]["name"] if object_class is None else object_class

        # remember to remove if clause (not its content) when writer's format (obj, score) is enforced on all indexers
        # start hack
        if key is None:
            key = self.get_identifier(objects, label_hash, du_hash, frame)
        # end hack

        row = {
            "identifier": key,
            "embedding": value,
            "description": description,
            "object_class": object_class,
            "frame": frame,
            "url": url,
        }

        self.writer.writerow(row)
        self.csv_file.flush()

        super().write_value(value)
