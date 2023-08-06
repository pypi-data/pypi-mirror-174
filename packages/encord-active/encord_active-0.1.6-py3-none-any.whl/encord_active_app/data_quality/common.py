from enum import Enum
from pathlib import Path
from typing import List, Union

import cv2
import numpy as np
import streamlit as st
from natsort import natsorted
from pandas import Series

from encord_active_app.common.colors import hex_to_rgb
from encord_active_app.common.indexer import IndexerData
from encord_active_app.common.utils import get_geometries, load_json, load_or_fill_image


class IndexType(Enum):
    DATA_QUALITY = "data_quality"
    LABEL_QUALITY = "label_quality"


def get_index_operation_level(pth: Path) -> str:
    if not all([pth.exists(), pth.is_file(), pth.suffix == ".csv"]):
        return ""

    with pth.open("r", encoding="utf-8") as f:
        _ = f.readline()  # Header, which we don't care about
        csv_row = f.readline()  # Content line

    if not csv_row:  # Empty index
        return ""

    key, _ = csv_row.split(",", 1)
    _, _, _, *object_hashes = key.split("_")
    return "O" if object_hashes else "F"


@st.experimental_memo
def load_available_indices(index_type_selection: IndexType) -> List[IndexerData]:
    def criterion(x):
        return x is None if index_type_selection == IndexType.DATA_QUALITY.value else x is not None

    indexer_dir = st.session_state.indexer_dir
    if not indexer_dir.is_dir():
        return []

    paths = natsorted([p for p in indexer_dir.iterdir() if p.suffix == ".csv"], key=lambda x: x.stem.split("_", 1)[1])
    levels = list(map(get_index_operation_level, paths))

    make_name = lambda p: p.name.split("_", 1)[1].rsplit(".", 1)[0].replace("_", " ").title()
    names = [f"{make_name(p)}" for p, l in zip(paths, levels)]
    meta_data = [load_json(f.with_suffix(".meta.json")) for f in paths]

    out: List[IndexerData] = []

    if not meta_data:
        return out

    for p, n, m, l in zip(paths, names, meta_data, levels):
        annotation_type = m.get("annotation_type")
        if m is None or not l or not criterion(annotation_type):
            continue

        out.append(IndexerData(name=n, path=p, meta=m, level=l))

    out = natsorted(out, key=lambda i: (i.level, i.name))  # type: ignore
    return out


def show_image_and_draw_polygons(row: Union[Series, str], draw_polygons: bool = True) -> np.ndarray:
    # === Read and annotate the image === #
    image = load_or_fill_image(row)

    # === Draw polygons / bboxes if available === #
    is_closed = True
    thickness = int(image.shape[1] / 150)

    if draw_polygons:
        for color, geometry in get_geometries(row):
            image = cv2.polylines(image, [geometry], is_closed, hex_to_rgb(color), thickness)

    return image
