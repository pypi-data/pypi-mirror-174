import json
from ast import literal_eval
from json import JSONDecodeError
from pathlib import Path
from typing import List, Optional, Tuple, Union

import cv2
import numpy as np
import pandas as pd
import streamlit as st

import encord_active_app.common.state as state
from encord_active_app.common.colors import Color, hex_to_rgb
from encord_active_app.common.css import write_page_css
from encord_active_app.common.state import load_project_tags, populate_session_state


def set_page_config():
    project_root = Path(__file__).parents[1]
    favicon_pth = project_root / "assets" / "favicon-32x32.png"
    st.set_page_config(
        page_title="Encord Active",
        layout="wide",
        page_icon=favicon_pth.as_posix(),
    )


def setup_page():
    populate_session_state()
    write_page_css()
    load_project_tags()


def load_json(json_file: Path) -> Optional[dict]:
    if not json_file.exists():
        return None

    with json_file.open("r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except JSONDecodeError:
            return None


def load_or_fill_image(row: Union[pd.Series, str]) -> np.ndarray:
    """
    Tries to read the infered image path. If not possible, generates a white image
    and indicates what the error seemd to be embedded in the image.
    :param row: A csv row from either an indexer, a prediction, or a label csv file.
    :return: Numpy / cv2 image.
    """

    done = False
    read_error = False
    key = __get_key(row)

    img_pth = key_to_image_path(key)

    if "not_available" not in img_pth.as_posix():
        # === Read and annotate the image === #
        image = cv2.imread(img_pth.as_posix())
        try:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        except cv2.error:
            read_error = True

        if not read_error:
            done = True

    if not done:
        label_hash, du_hash, frame, *_ = key.split("_")
        lr_path = key_to_lr_path(key)

        with lr_path.open("r", encoding="utf-8") as f:
            lr = json.load(f)
        du = lr["data_units"][du_hash]
        w, h = du["width"], du["height"]

        image = np.ones((h, w, 3), dtype=np.uint8) * 255
        font = cv2.FONT_HERSHEY_SIMPLEX
        txt = "Image seems to be broken" if read_error else "Image not downloaded"
        cv2.putText(image, txt, (25, 25), font, 1.0, hex_to_rgb("#999999"), 2, cv2.LINE_AA)

    return image


class PageTracker:
    def __init__(self, page_state: int):
        self.page_state = page_state

    def reset_page_state(self):
        self.page_state = 1


def get_df_subset(df: pd.DataFrame, selected_index: Optional[str]):
    if selected_index not in df:
        return df

    max_val = float(df[selected_index].max()) + np.finfo(float).eps.item()
    min_val = float(df[selected_index].min())

    if max_val <= min_val:
        return df

    start, end = st.slider("Choose quality", max_value=max_val, min_value=min_val, value=(min_val, max_val))
    subset = df[df[selected_index].between(start, end)]

    return subset


def build_pagination(subset, n_cols, n_rows, selected_index):
    n_items = n_cols * n_rows
    col1, col2 = st.columns(spec=[1, 4])

    with col1:
        sorting_order = st.selectbox("Sort samples within selected interval", ["Descending", "Ascending"])

    with col2:
        last = len(subset) // n_items + 1
        page_num = st.slider("Page", 1, last) if last > 1 else 1

    low_lim = (page_num - 1) * n_items
    high_lim = page_num * n_items

    sorted_subset = subset.sort_values(by=selected_index, ascending=sorting_order == "Ascending")
    paginated_subset = sorted_subset[low_lim:high_lim]
    return paginated_subset


def __get_key(row: Union[pd.Series, str]):
    if isinstance(row, pd.Series):
        if "identifier" not in row:
            raise ValueError("A Series passed but the series doesn't contain 'identifier'")
        return str(row["identifier"])
    elif isinstance(row, str):
        return row
    else:
        raise Exception(f"Undefined row type {row}")


def __get_geometry(obj: dict, w: int, h: int) -> Optional[Tuple[str, np.ndarray]]:
    """
    Convert Encord object dictionary to polygon coordinates used to draw geometries
    with opencv.

    :param obj: the encord object dict
    :param w: the image width
    :param h: the image height
    :return: The polygon coordinates
    """

    if obj["shape"] == "polygon":
        p = obj["polygon"]
        polygon = np.array([[p[str(i)]["x"] * w, p[str(i)]["y"] * h] for i in range(len(p))])
    elif obj["shape"] == "bounding_box":
        b = obj["boundingBox"]
        polygon = np.array(
            [
                [b["x"] * w, b["y"] * h],
                [(b["x"] + b["w"]) * w, b["y"] * h],
                [(b["x"] + b["w"]) * w, (b["y"] + b["h"]) * h],
                [b["x"] * w, (b["y"] + b["h"]) * h],
            ]
        )
    else:
        return None

    polygon = polygon.reshape((-1, 1, 2)).astype(int)
    return obj.get("color", Color.PURPLE.value), polygon


def get_geometries(row: Union[pd.Series, str]) -> List[Tuple[str, np.ndarray]]:
    """
    Loads cached label row and computes geometries from the label row.
    If the ``identifier`` in the ``row`` contains an object hash, only that object will
    be drawn. If no object hash exists, all polygons / bboxes will be drawn.
    :param row: the pandas row of the selected csv file.
    :return: List of tuples of (hex color, polygon: [[x, y], ...])
    """
    key = __get_key(row)
    _, du_hash, frame, *remainder = key.split("_")

    lr_pth = key_to_lr_path(key)
    with lr_pth.open("r") as f:
        label_row = json.load(f)

    du = label_row["data_units"][du_hash]

    if "width" not in du or "height" not in du:
        image = cv2.imread(key_to_image_path(key).as_posix())
        h = image.shape[0]
        w = image.shape[1]
    else:
        w = int(du["width"])
        h = int(du["height"])

    geometries = []
    if "video" not in du["data_type"]:
        if remainder:
            # Return specific geometries
            geometry_object_hashes = set(remainder)
            for obj in du["labels"]["objects"]:
                if obj["objectHash"] in geometry_object_hashes:
                    geometries.append(__get_geometry(obj, w, h))
        else:
            # Get all geometries
            for obj in du["labels"]["objects"]:
                if obj["shape"] not in {"polygon", "bounding_box"}:
                    continue
                geometries.append(__get_geometry(obj, w, h))
    else:
        if remainder:
            # Return specific geometries
            geometry_object_hashes = set(remainder)
            for obj in du["labels"][str(int(frame))]["objects"]:
                if obj["objectHash"] in geometry_object_hashes:
                    geometries.append(__get_geometry(obj, w, h))
        else:
            # Get all geometries
            for obj in du["labels"][str(int(frame))]["objects"]:
                if obj["shape"] not in {"polygon", "bounding_box"}:
                    continue
                geometries.append(__get_geometry(obj, w, h))

    valid_geometries = list(filter(None, geometries))
    return valid_geometries


def key_to_lr_path(key: str) -> Path:
    label_hash, *_ = key.split("_")
    return st.session_state.data_dir / label_hash / "label_row.json"


def key_to_image_path(key: str) -> Path:
    """
    Infer image path from the identifier stored in the csv files.
    :param key: the row["identifier"] from a csv row
    :return: The associated image path if it exists or a path to a placeholder otherwise
    """
    label_hash, du_hash, frame, *_ = key.split("_")
    img_folder = st.session_state.data_dir / label_hash / "images"

    # check if it is a video frame
    frame_pth = list(img_folder.glob(f"{du_hash}_{int(frame)}.*"))
    if len(frame_pth) == 0:
        img_pth = next(img_folder.glob(f"{du_hash}.*"))  # So this is an img_group image

        if not img_pth.exists():
            img_pth = Path(__file__).parent / "resources" / "Image_not_available.jpeg"
    else:
        img_pth = frame_pth[0]
    return img_pth


def merge_all_available_metrics(index_path: Path) -> pd.DataFrame:
    main_df = pd.DataFrame(columns=["identifier"])
    for index in index_path.glob("*.csv"):
        meta_pth = index.with_suffix(".meta.json")
        if not meta_pth.is_file():
            continue

        with meta_pth.open("r", encoding="utf-8") as f:
            meta = json.load(f)

        indexer_scores = pd.read_csv(index)
        if indexer_scores.shape[0] == 0:
            continue

        columns_to_merge = indexer_scores[["identifier", "score"]]
        main_df = pd.merge(main_df, columns_to_merge, how="outer", on="identifier")
        main_df.rename(columns={"score": f"{meta['title']}"}, inplace=True)

    return main_df


def load_merged_df():
    if state.MERGED_DATAFRAME not in st.session_state:
        if st.session_state.merged_df_filepath.is_file():
            merged_df = pd.read_csv(st.session_state.merged_df_filepath, converters={"tags": literal_eval})
        else:
            # If merged_df file is not exist create one and save
            merged_df = merge_all_available_metrics(st.session_state.indexer_dir)
            merged_df["tags"] = [[] for i in range(merged_df.shape[0])]
            merged_df.to_csv(st.session_state.merged_df_filepath, index=False)

        st.session_state[state.MERGED_DATAFRAME] = merged_df
