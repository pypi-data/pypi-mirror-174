import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple, cast

import pandas as pd
import streamlit as st
from natsort import natsorted

from encord_active_app.common.utils import load_json


def check_model_prediction_availability():
    predictions_path = st.session_state.predictions_dir / "predictions.csv"
    return predictions_path.is_file()


def merge_objects_and_scores(
    object_df: pd.DataFrame, index_pth: Optional[Path] = None, ignore_object_scores=True
) -> Tuple[pd.DataFrame, List[str]]:
    indexer_names: List[str] = []
    object_df["identifier_no_oh"] = object_df["identifier"].str.replace(r"^(\S{73}_\d+)(.*)", r"\1", regex=True)

    if index_pth is not None:
        # Import prediction scores
        for index in index_pth.iterdir():
            if not index.suffix == ".csv":
                continue

            meta_pth = index.with_suffix(".meta.json")
            if not meta_pth.is_file():
                continue

            with meta_pth.open("r", encoding="utf-8") as f:
                meta = json.load(f)

            indexer_scores = pd.read_csv(index, index_col="identifier")
            # Ignore empty data frames.
            if indexer_scores.shape[0] == 0:
                continue

            title = f"{meta['title']} (P)"
            indexer_names.append(title)

            has_object_level_keys = len(indexer_scores.index[0].split("_")) > 3
            indexer_column = "identifier" if has_object_level_keys else "identifier_no_oh"
            # Join data and rename column to indexer name.
            object_df = object_df.join(indexer_scores["score"], on=[indexer_column])
            object_df[title] = object_df["score"]
            object_df.drop("score", axis=1, inplace=True)

    # Import frame level scores
    for index_file in st.session_state.indexer_dir.iterdir():
        if index_file.is_dir() or index_file.suffix != ".csv":
            continue

        # Read first row to see if index has frame level scores
        with index_file.open("r", encoding="utf-8") as f:
            f.readline()  # header
            key, *_ = f.readline().split(",")

        if not key:  # Empty index
            continue

        label_hash, du_hash, frame, *rest = key.split("_")
        type_indicator = "F"  # Frame level
        join_column = "identifier_no_oh"
        if rest and ignore_object_scores:
            # There are object hashes included in the key, so ignore.
            continue
        elif rest:
            type_indicator = "O"
            join_column = "identifier"

        meta_pth = index_file.with_suffix(".meta.json")
        if not meta_pth.is_file():
            continue

        with meta_pth.open("r", encoding="utf-8") as f:
            meta = json.load(f)

        indexer_scores = pd.read_csv(index_file, index_col="identifier")

        title = f"{meta['title']} ({type_indicator})"
        indexer_names.append(title)

        # Join data and rename column to indexer name.
        object_df = object_df.join(indexer_scores["score"], on=join_column)
        object_df[title] = object_df["score"]
        object_df.drop("score", axis=1, inplace=True)
    object_df.drop("identifier_no_oh", axis=1, inplace=True)
    indexer_names = cast(List[str], natsorted(indexer_names, key=lambda x: x[-3:] + x[:-3]))
    return object_df, indexer_names


@st.cache(allow_output_mutation=True)
def get_model_predictions() -> Optional[Tuple[pd.DataFrame, List[str]]]:
    """
    Loads predictions and their associated indexer scores.
    :param predictions_path:
    :return:
        - predictions: The predictions with their indexer scores
        - column names: Unit test column names.
    """
    predictions_path = st.session_state.predictions_dir / "predictions.csv"
    if not predictions_path.is_file():
        return None

    predictions_df = pd.read_csv(predictions_path)

    # Extract label_hash, du_hash, frame
    identifiers = predictions_df["identifier"].str.split("_", expand=True)
    identifiers.columns = ["label_hash", "du_hash", "frame", "object_hash"][: len(identifiers.columns)]
    identifiers["frame"] = pd.to_numeric(identifiers["frame"])
    predictions_df = pd.concat([predictions_df, identifiers], axis=1)

    # Load predictions scores (indexers)
    pred_idx_pth = st.session_state.predictions_dir / "indexes"
    if not pred_idx_pth.exists():
        return predictions_df, []

    predictions_df, indexer_names = merge_objects_and_scores(predictions_df, index_pth=pred_idx_pth)

    return predictions_df, indexer_names


@st.cache(allow_output_mutation=True)
def get_labels() -> Optional[Tuple[pd.DataFrame, List[str]]]:
    labels_path = st.session_state.predictions_dir / "labels.csv"
    if not labels_path.is_file():
        return None

    labels_df = pd.read_csv(labels_path)

    # Extract label_hash, du_hash, frame
    identifiers = labels_df["identifier"].str.split("_", expand=True)
    identifiers = identifiers.iloc[:, :3]
    identifiers.columns = ["label_hash", "du_hash", "frame"]
    identifiers["frame"] = pd.to_numeric(identifiers["frame"])

    labels_df = pd.concat([labels_df, identifiers], axis=1)
    labels_df, label_indexer_names = merge_objects_and_scores(labels_df, ignore_object_scores=False)
    return labels_df, label_indexer_names


@st.cache(allow_output_mutation=True)
def get_gt_matched() -> Optional[dict]:
    gt_path = st.session_state.predictions_dir / "ground_truths_matched.json"
    return load_json(gt_path)


@st.cache()
def get_class_idx() -> Optional[dict]:
    class_idx_pth = st.session_state.predictions_dir / "class_idx.json"
    return load_json(class_idx_pth)


@st.cache()
def get_metadata_files() -> Dict[str, dict]:
    out: Dict[str, dict] = {}
    # Look in data indexers
    data_indexers = out.setdefault("data", {})
    if st.session_state.indexer_dir.is_dir():
        for f in st.session_state.indexer_dir.iterdir():
            if not f.name.endswith(".meta.json"):
                continue

            meta = load_json(f)
            if meta is None:
                continue

            data_indexers[meta["title"]] = meta

    prediction_indexers = out.setdefault("prediction", {})
    if (st.session_state.predictions_dir / "indexes").is_dir():
        for f in st.session_state.indexer_dir.iterdir():
            if not f.name.endswith(".meta.json"):
                continue

            meta = load_json(f)
            if meta is None:
                continue

            prediction_indexers[meta["title"]] = meta

    return out


def filter_labels_for_frames_wo_predictions():
    """
    Note: data_root is not used in the code, but utilized by `st` to determine what
    to cache, so please don't remove.
    """
    _predictions = st.session_state.model_predictions
    pred_keys = _predictions["img_id"].unique()
    _labels = st.session_state.sorted_labels
    return _labels[_labels["img_id"].isin(pred_keys)]


def prediction_and_label_filtering(labels, metrics, model_pred, precisions):
    # Filtering based on selection
    # In the following a "_" prefix means the the data has been filtered according to selected classes.
    # Predictions
    class_idx = st.session_state.selected_class_idx
    row_selection = model_pred["class_id"].isin(set(map(int, class_idx.keys())))
    _model_pred = model_pred[row_selection].copy()
    # Labels
    row_selection = labels["class_id"].isin(set(map(int, class_idx.keys())))
    _labels = labels[row_selection]

    chosen_name_set = set(map(lambda x: x["name"], class_idx.values())).union({"Mean"})
    _metrics = metrics[metrics["class_name"].isin(chosen_name_set)]
    _precisions = precisions[precisions["class_name"].isin(chosen_name_set)]
    name_map = {int(k): v["name"] for k, v in class_idx.items()}
    _model_pred["class_name"] = _model_pred["class_id"].map(name_map)
    return _labels, _metrics, _model_pred, _precisions
