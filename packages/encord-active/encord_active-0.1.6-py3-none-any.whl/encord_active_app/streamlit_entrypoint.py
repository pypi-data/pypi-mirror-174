import argparse
from functools import reduce
from typing import Callable, Dict, Optional, Union

import streamlit as st
import streamlit_nested_layout  # pylint: disable=unused-import

from encord_active_app.common import state
from encord_active_app.common.utils import set_page_config
from encord_active_app.data_quality.common import IndexType
from encord_active_app.frontend_components import pages_menu
from encord_active_app.model_assertions.sub_pages.false_negatives import (
    FalseNegativesPage,
)
from encord_active_app.model_assertions.sub_pages.false_positives import (
    FalsePositivesPage,
)
from encord_active_app.model_assertions.sub_pages.metrics import MetricsPage
from encord_active_app.model_assertions.sub_pages.performance_by_index import (
    PerformanceIndex,
)
from encord_active_app.model_assertions.sub_pages.true_positives import (
    TruePositivesPage,
)
from encord_active_app.views.export import export
from encord_active_app.views.getting_started import getting_started
from encord_active_app.views.indexes import explorer, summary
from encord_active_app.views.model_assertions import model_assertions

Pages = Dict[str, Union[Callable, "Pages"]]  # type: ignore

pages: Pages = {
    "Getting Started": getting_started,
    "Data Quality": {"Summary": summary(IndexType.DATA_QUALITY), "Explorer": explorer(IndexType.DATA_QUALITY)},
    "Label Quality": {"Summary": summary(IndexType.LABEL_QUALITY), "Explorer": explorer(IndexType.LABEL_QUALITY)},
    "Model Assertions": {
        "Metrics": model_assertions(MetricsPage()),
        "Performance By Indexer": model_assertions(PerformanceIndex()),
        "True Positives": model_assertions(TruePositivesPage()),
        "False Positives": model_assertions(FalsePositivesPage()),
        "False Negatives": model_assertions(FalseNegativesPage()),
    },
    "Actions": export,
}

SEPARATOR = "#"


def to_item(k, v, parent_key: Optional[str] = None):
    # NOTE: keys must be unique for the menu to render properly
    composite_key = SEPARATOR.join(filter(None, [parent_key, k]))
    item = {"key": composite_key, "label": k}
    if isinstance(v, dict):
        item["children"] = to_items(v, parent_key=composite_key)
    return item


def to_items(d: dict, parent_key: Optional[str] = None):
    return [to_item(k, v, parent_key) for k, v in d.items()]


def main(project_path: str):
    set_page_config()

    if not state.set_project_dir(project_path):
        st.error(f"Project not found for directory `{project_path}`.")

    with st.sidebar:
        items = to_items(pages)
        key = pages_menu(items=items)
        path = key.split(SEPARATOR) if key else []

    render = reduce(dict.__getitem__, path, pages) if path else pages["Getting Started"]  # type: ignore
    if callable(render):
        render()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("project_dir", type=str, help="Directory in which your project data is stored")
    args = parser.parse_args()
    main(args.project_dir)
