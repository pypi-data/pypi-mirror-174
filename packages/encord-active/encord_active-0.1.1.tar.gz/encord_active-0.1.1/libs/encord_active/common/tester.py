import json
import logging
from enum import Enum
from pathlib import Path
from typing import Any, List, Type, Union

from encord_active.common.indexer import Indexer
from encord_active.common.iterator import DatasetIterator, Iterator
from encord_active.common.utils import fetch_project_info
from encord_active.common.writer import CSVIndexWriter, StatisticsObserver
from loguru import logger

logger = logger.opt(colors=True)


def __get_value(o):
    if isinstance(o, (float, int, str)):
        return o
    if isinstance(o, Enum):
        return __get_value(o.value)
    if isinstance(o, (list, tuple)):
        return [__get_value(v) for v in o]
    return None


def __get_object_attributes(obj: Any):
    indexer_properties = {v.lower(): __get_value(getattr(obj, v)) for v in dir(obj)}
    indexer_properties = {k: v for k, v in indexer_properties.items() if (v is not None or k == "annotation_type")}
    return indexer_properties


@logger.catch()
def perform_test(
    indexers: Union[Indexer, List[Indexer]],
    data_dir: Path,
    iterator_cls: Type[Iterator] = DatasetIterator,
    **kwargs,
):
    all_tests: List[Indexer] = indexers if isinstance(indexers, list) else [indexers]

    project = fetch_project_info(data_dir)
    # take into account possible kwargs parameters
    use_images = any([test.NEEDS_IMAGES for test in all_tests] + [kwargs.get("use_images", False)])
    kwargs.pop("use_images", None)  # drop 'use_image' to avoid multiple values for the same keyword argument
    iterator = iterator_cls(project, data_dir, use_images=use_images, **kwargs)
    cache_dir = iterator.update_cache_dir(data_dir)

    for indexer in all_tests:
        logger.info(f"Running Indexer <blue>{indexer.TITLE.title()}</blue>")
        unique_indexer_name = indexer.get_unique_name()

        stats = StatisticsObserver()
        with CSVIndexWriter(cache_dir, iterator, prefix=unique_indexer_name) as writer:
            writer.attach(stats)

            try:
                indexer.test(iterator, writer)
            except Exception as e:
                logging.critical(e, exc_info=True)

        # Store meta-data about the scores.
        meta_file = (cache_dir / "indexes" / f"{unique_indexer_name}.meta.json").expanduser()

        with meta_file.open("w") as f:
            json.dump(
                {
                    **__get_object_attributes(indexer),
                    **__get_object_attributes(stats),
                },
                f,
                indent=2,
            )
