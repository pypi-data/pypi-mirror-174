from pathlib import Path

import streamlit as st
import yaml

# CONSTANTS
PROJECT_CACHE_FILE = Path.home() / ".encord_assertions" / "current_project_dir.txt"
PROJECT_TAGS_FILE_NAME = "project_tags.yaml"
MERGED_DF_FILENAME = "merged_metrics.csv"

# STATE VARIABLE KEYS
CLASS_SELECTION = "class_selection"
IGNORE_FRAMES_WO_PREDICTIONS = "ignore_frames_wo_predictions"
INDEXER_NAME = "indexer_name"
IOU_THRESHOLD = "iou_threshold_scaled"  # After normalization
IOU_THRESHOLD_ = "iou_threshold_"  # Before normalization
MERGED_DATAFRAME = "merged_dataframe"
PROJECT_TAGS = "project_tags"
PROJECT_TAGS_FILE_PATH = "project_tags_file_path"
PROJECT_PREVIOUS_TAGS = "project_previous_tags"

# DATA QUALITY PAGE
DATA_PAGE_TYPE = "data_page_type"  # Summary | Explorer
DATA_PAGE_INDEX_TYPE = "data_page_index_type"  # Label quality | Data Quality
DATA_PAGE_INDEX = "data_page_index"  # index
DATA_PAGE_INDEX_NAME = "data_page_index_name"  # index name
DATA_PAGE_CLASS = "data_page_class_selection"  # class
DATA_PAGE_ANNOTATOR = "data_page_annotator_selection"  # annotator
DATA_PAGE_BUILDER = "data_page_builder"  # index builder callable


# PREDICTIONS PAGE
PREDICTIONS_LABEL_INDEX = "predictions_label_index"
PREDICTIONS_DECOMPOSE_CLASSES = "predictions_decompose_classes"
PREDICTIONS_INDEX = "predictions_index"
PREDICTIONS_NBINS = "predictions_nbins"
PREDICTIONS_PAGE_SELECTION = "predictions_page_selection"
PREDICTIONS_SHOW_DOWNLOAD_BUTTON = "predictions_show_download_button"

# TILING & PAGINATION
MAIN_VIEW_COLUMN_NUM = "main_view_column_num"
MAIN_VIEW_ROW_NUM = "main_view_row_num"
K_NEAREST_NUM = "k_nearest_num"

IDENTIFIER_TO_NEIGHBORS_CLASSES = "identifier_to_neighbors_classes"
IDENTIFIER_TO_NEIGHBORS_OBJECTS = "identifier_to_neighbors_objects"
QUESTION_HASH_TO_COLLECTION_INDEXES = "question_hash_to_collection_indexes"
COLLECTIONS = "collections"

DATA_PAGE_NUMBER = "data_page_number"
INDEX_VIEW_PAGE_NUMBER = "index_view_page_number"
FALSE_NEGATIVE_VIEW_PAGE_NUMBER = "false_negative_view_page_number"

NORMALIZATION_STATUS = "normalization_status"
PREVIOUS_INDEX_TITLE = "previous_index_title"
INDEX_METADATA_SCORE_NORMALIZATION = "score_normalization"
INDEX_METADATA_TITLE = "title"
INDEX_METADATA_NUM_ROWS = "num_rows"
INDEX_METADATA_DATA_TYPE = "data_type"
TOTAL_UNIQUE_CLASSES = "total_unique_classes"
TOTAL_UNIQUE_IMAGES = "total_unique_images"


def set_project_dir(project_dir: str) -> bool:
    _project_dir = Path(project_dir).expanduser().absolute()

    if not _project_dir.is_dir():
        return False
    else:
        PROJECT_CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
        with PROJECT_CACHE_FILE.open("w", encoding="utf-8") as f:
            f.write(_project_dir.as_posix())
        st.session_state.project_dir = _project_dir
        return True


def populate_session_state():
    if "project_dir" not in st.session_state:
        # Try using a cached one
        if PROJECT_CACHE_FILE.is_file():
            with PROJECT_CACHE_FILE.open("r", encoding="utf-8") as f:
                st.session_state.project_dir = Path(f.readline())

    st.session_state.indexer_dir = st.session_state.project_dir / "indexes"
    st.session_state.embeddings_dir = st.session_state.project_dir / "embeddings"
    st.session_state.predictions_dir = st.session_state.project_dir / "predictions"
    st.session_state.data_dir = st.session_state.project_dir / "data"
    st.session_state.merged_df_filepath = st.session_state.project_dir / MERGED_DF_FILENAME
    # TODO Data directory may vary now depending on the user.


def load_project_tags():
    project_tags_file_path = st.session_state.project_dir / PROJECT_TAGS_FILE_NAME
    st.session_state[PROJECT_TAGS_FILE_PATH] = project_tags_file_path
    if project_tags_file_path.is_file():
        with project_tags_file_path.open("r", encoding="utf-8") as f:
            project_tags = yaml.safe_load(f)
            st.session_state[PROJECT_TAGS] = project_tags["tags"]
    else:
        with project_tags_file_path.open("w", encoding="utf-8") as f:
            project_tags = {"tags": []}
            f.write(yaml.dump(project_tags))
            st.session_state[PROJECT_TAGS] = project_tags["tags"]
