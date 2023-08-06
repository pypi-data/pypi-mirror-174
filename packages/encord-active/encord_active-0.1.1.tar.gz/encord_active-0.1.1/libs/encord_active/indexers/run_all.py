import inspect
import logging
import os
from importlib import import_module
from typing import Callable, List, Optional, Union

from encord_active.common.indexer import AnnotationType, DataType, Indexer, IndexType
from encord_active.common.tester import perform_test


def get_indexers(module: Optional[Union[str, list[str]]] = None, filter_func=lambda x: True):
    if module is None:
        module = ["geometric", "heuristic", "semantic"]

    indexers = []
    if isinstance(module, list):  # type: ignore
        for module in module:
            indexers.extend(get_indexers(module, filter_func))
    else:
        indexers.extend(get_module_indexers(module, filter_func))

    return indexers


def get_module_indexers(module_name: str, filter_func: Callable) -> List:
    base_module_name = __name__[: __name__.rindex(".")]  # Remove "run_all"
    indexers = []
    path = os.path.join(os.path.dirname(__file__), *module_name.split("."))
    for file in os.listdir(path):
        if file.endswith(".py") and not file.startswith("_") and not file.split(".")[0].endswith("_"):
            logging.info("Importing %s", file)
            clsmembers = inspect.getmembers(
                import_module(f"{base_module_name}.{module_name}.{file.split('.')[0]}"), inspect.isclass
            )
            for cls in clsmembers:
                if issubclass(cls[1], Indexer) and cls[1] != Indexer and filter_func(cls[1]):
                    indexers.append((f"{base_module_name}.{module_name}.{file.split('.')[0]}", f"{cls[0]}"))

    return indexers


def run_all_heuristic_indexers():
    run_indexers(filter_func=lambda x: x.INDEX_TYPE == IndexType.HEURISTIC)


def run_all_image_indexers():
    run_indexers(filter_func=lambda x: x.DATA_TYPE == DataType.IMAGE)


def run_all_polygon_indexers():
    run_indexers(filter_func=lambda x: x.ANNOTATION_TYPE in [AnnotationType.OBJECT.POLYGON, AnnotationType.ALL])


def run_indexers(filter_func: Callable = lambda x: True, **kwargs):
    indexers: List[Indexer] = list(
        map(
            lambda mod_cls: import_module(mod_cls[0]).__getattribute__(mod_cls[1])(),
            get_indexers(filter_func=filter_func),
        )
    )
    perform_test(indexers, **kwargs)


if __name__ == "__main__":
    # To run on all samples:
    import os
    from pathlib import Path

    import yaml
    from encord import EncordUserClient

    conf_file = Path(__file__).parents[0] / "conf" / "config.yaml"
    if conf_file.is_file():
        # Fallback to read old config file and store it in new format, directly in the
        # data directory instead of in the code root.
        with conf_file.open("r", encoding="utf-8") as f:
            conf = yaml.safe_load(f)

        data_dir = conf["paths"]["data"]
        private_key_path = conf["paths"]["private_key"]
        project_name = conf["encord"]["project_name"]

        with open(os.path.expanduser(private_key_path), "r", encoding="utf-8") as f:
            private_key = f.read()

        client = EncordUserClient.create_with_ssh_private_key(private_key)
        project_desc = client.get_projects(title_eq=project_name)[0]["project"]
        project = client.get_project(project_hash=project_desc.project_hash)
        project_name = f"{project.project_hash[:8]}_{project.title.replace(' ', '-').lower()}"
        project_root = Path(data_dir).expanduser() / project_name

        project_meta = {
            "project_title": project.title,
            "project_description": project.description,
            "project_hash": project.project_hash,
            "ssh_key_path": os.path.abspath(os.path.expanduser(private_key_path)),
        }
        meta_file_path = project_root / "project_meta.yaml"
        with meta_file_path.open("w", encoding="utf-8") as f:
            f.write(yaml.dump(project_meta))
    else:
        # Just specify a project root by input.
        project_root = Path(input("Choose data root: ")).expanduser().absolute()

    run_indexers(data_dir=project_root)
