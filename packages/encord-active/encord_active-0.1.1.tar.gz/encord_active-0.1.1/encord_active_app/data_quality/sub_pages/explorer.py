import re
from typing import List

import altair as alt
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
from encord_active.common.indexer import AnnotationType, EmbeddingType
from natsort import natsorted
from pandas import Series
from streamlit.delta_generator import DeltaGenerator

import encord_active_app.common.state as state
from encord_active_app.common import embedding_utils
from encord_active_app.common.components import (
    build_data_tags,
    multiselect_with_all_option,
)
from encord_active_app.common.components.bulk_tagging_form import (
    BulkLevel,
    action_bulk_tags,
    bulk_tagging_form,
)
from encord_active_app.common.components.indivdual_tagging import (
    multiselect_tag,
    tag_creator,
)
from encord_active_app.common.indexer import IndexerData, load_index
from encord_active_app.common.page import Page
from encord_active_app.common.utils import (
    build_pagination,
    get_df_subset,
    load_merged_df,
)
from encord_active_app.data_quality.common import (
    load_or_fill_image,
    show_image_and_draw_polygons,
)


class ExplorerPage(Page):
    title = "🔎 Explorer"

    def sidebar_options(self, available_indices: List[IndexerData]):
        load_merged_df()
        tag_creator()

        if not available_indices:
            st.error("Your data has not been indexed. Make sure you have imported your data correctly.")
            st.stop()

        non_empty_indices = [index for index in available_indices if not load_index(index, normalize=False).empty]
        sorted_indices = sorted(non_empty_indices, key=lambda i: i.name)

        indexer_names = list(map(lambda i: i.name, sorted_indices))

        col1, col2, col3 = st.columns(3)
        selected_indexer_name = col1.selectbox(
            "Select an index to order your data by",
            indexer_names,
            help="The data in the main view will be sorted by the selected indexer. ",
        )

        indexer_idx = indexer_names.index(selected_indexer_name)
        st.session_state[state.DATA_PAGE_INDEX] = sorted_indices[indexer_idx]
        st.session_state[state.DATA_PAGE_INDEX_NAME] = selected_indexer_name

        if state.NORMALIZATION_STATUS not in st.session_state:
            st.session_state[state.NORMALIZATION_STATUS] = st.session_state[state.DATA_PAGE_INDEX].meta.get(
                state.INDEX_METADATA_SCORE_NORMALIZATION, True
            )  # If there is no information on the meta file, just normalize (its probability is higher)

        df = load_index(st.session_state[state.DATA_PAGE_INDEX], normalize=st.session_state[state.NORMALIZATION_STATUS])

        if df.shape[0] > 0:
            class_set = sorted(list(df["object_class"].unique()))
            with col2:
                selected_classes = multiselect_with_all_option("Filter by class", class_set, key=state.DATA_PAGE_CLASS)

            is_class_selected = (
                df.shape[0] * [True] if "All" in selected_classes else df["object_class"].isin(selected_classes)
            )
            df_class_selected = df[is_class_selected]

            annotators = get_annotator_level_info(df_class_selected)
            annotator_set = sorted(annotators["annotator"])

            with col3:
                selected_annotators = multiselect_with_all_option(
                    "Filter by annotator",
                    annotator_set,
                    key=state.DATA_PAGE_ANNOTATOR,
                )

            annotator_selected = (
                df_class_selected.shape[0] * [True]
                if "All" in selected_annotators
                else df_class_selected["annotator"].isin(selected_annotators)
            )

            self.row_col_settings_in_sidebar()

            # For now go the easy route and just filter the dataframe here
            return df_class_selected[annotator_selected]

    def build(self, selected_df: pd.DataFrame):
        st.markdown(f"# {self.title}")
        meta = st.session_state[state.DATA_PAGE_INDEX].meta
        st.markdown(f"## {meta['title']}")
        st.markdown(meta["long_description"])

        if selected_df.empty:
            return

        fill_dataset_properties_window(selected_df)
        fill_annotator_properties_window(selected_df)
        fill_data_quality_window(selected_df)


def get_annotator_level_info(df: pd.DataFrame) -> dict[str, list]:
    annotator_set = natsorted(list(df["annotator"].unique()))
    annotators: dict[str, list] = {"annotator": annotator_set, "total annotation": [], "score": []}

    for annotator in annotator_set:
        annotators["total annotation"].append(df[df["annotator"] == annotator].shape[0])
        annotators["score"].append(df[df["annotator"] == annotator]["score"].mean())

    return annotators


def fill_dataset_properties_window(current_df: pd.DataFrame):
    dataset_expander = st.expander("Dataset Properties", expanded=True)
    dataset_columns = dataset_expander.columns(3)

    cls_set = natsorted(list(current_df["object_class"].unique()))

    dataset_columns[0].metric("Number of labels", current_df.shape[0])
    dataset_columns[1].metric("Number of classes", len(cls_set))
    dataset_columns[2].metric("Number of images", get_unique_data_units_size(current_df))

    if len(cls_set) > 1:
        classes = {}
        for cls in cls_set:
            classes[cls] = (current_df["object_class"] == cls).sum()

        source = pd.DataFrame({"class": list(classes.keys()), "count": list(classes.values())})

        fig = px.bar(source, x="class", y="count")
        fig.update_layout(title_text="Distribution of the classes", title_x=0.5, title_font_size=20)
        dataset_expander.plotly_chart(fig, use_container_width=True)


def fill_annotator_properties_window(current_df: pd.DataFrame):
    annotators = get_annotator_level_info(current_df)
    if not (len(annotators["annotator"]) == 1 and (not isinstance(annotators["annotator"][0], str))):
        annotator_expander = st.expander("Annotator Statistics", expanded=False)

        annotator_columns = annotator_expander.columns([2, 2])

        # 1. Pie Chart
        annotator_columns[0].markdown(
            "<h5 style='text-align: center; color: black;'>Distribution of the annotations</h1>", unsafe_allow_html=True
        )
        source = pd.DataFrame(
            {
                "annotator": annotators["annotator"],
                "total": annotators["total annotation"],
                "score": [f"{score:.3f}" for score in annotators["score"]],
            }
        )

        fig = px.pie(source, values="total", names="annotator", hover_data=["score"])
        # fig.update_layout(title_text="Distribution of the annotations", title_x=0.5, title_font_size=20)

        annotator_columns[0].plotly_chart(fig, use_container_width=True)

        # 2. Table View
        annotator_columns[1].markdown(
            "<h5 style='text-align: center; color: black;'>Detailed annotator statistics</h1>", unsafe_allow_html=True
        )

        annotators["annotator"].append("all")
        annotators["total annotation"].append(current_df.shape[0])

        df_mean_score = current_df["score"].mean()
        annotators["score"].append(df_mean_score)
        deviations = 100 * ((np.array(annotators["score"]) - df_mean_score) / df_mean_score)
        annotators["deviations"] = deviations
        annotators_df = pd.DataFrame.from_dict(annotators)

        def _format_deviation(val):
            return f"{val:.1f}%"

        def _format_score(val):
            return f"{val:.3f}"

        def _color_red_or_green(val):
            color = "red" if val < 0 else "green"
            return f"color: {color}"

        def make_pretty(styler):
            styler.format(_format_deviation, subset=["deviations"])
            styler.format(_format_score, subset=["score"])
            styler.applymap(_color_red_or_green, subset=["deviations"])
            return styler

        annotator_columns[1].dataframe(annotators_df.style.pipe(make_pretty), use_container_width=True)


def fill_data_quality_window(current_df: pd.DataFrame):
    annotation_type = st.session_state[state.DATA_PAGE_INDEX].meta.get("annotation_type")
    if (
        (annotation_type is None)
        or (len(annotation_type) == 1 and annotation_type[0] == str(AnnotationType.CLASSIFICATION.RADIO.value))
        or (
            st.session_state[state.DATA_PAGE_INDEX].meta.get("title")
            in [
                "Frame object density",
                "Object Count",
            ]
        )
    ):  # TODO find a better way to filter these later because titles can change
        embedding_type = str(EmbeddingType.CLASSIFICATION.value)
    else:
        embedding_type = str(EmbeddingType.OBJECT.value)

    populate_embedding_information(embedding_type)
    if len(st.session_state[state.COLLECTIONS]) == 0:
        st.write("Embedding file is not available for this project")
    else:
        n_cols = int(st.session_state[state.MAIN_VIEW_COLUMN_NUM])
        n_rows = int(st.session_state[state.MAIN_VIEW_ROW_NUM])

        chart = get_histogram(current_df)
        st.altair_chart(chart, use_container_width=True)
        subset = get_df_subset(current_df, "score")

        st.write(f"Interval contains {subset.shape[0]} of {current_df.shape[0]} annotations")

        paginated_subset = build_pagination(subset, n_cols, n_rows, "score")

        form = bulk_tagging_form()

        if form and form.submitted:
            df = paginated_subset if form.level == BulkLevel.PAGE else subset
            action_bulk_tags(df, form.tags, form.action)

        if len(paginated_subset) == 0:
            st.error("No data in selected interval")
        else:
            cols: List = []
            similarity_expanders = []
            for i, (row_no, row) in enumerate(paginated_subset.iterrows()):
                if not cols:
                    cols = list(st.columns(n_cols))
                    similarity_expanders.append(st.expander("Similarities", expanded=True))

                with cols.pop(0):
                    build_card(embedding_type, i, row, similarity_expanders)


def populate_embedding_information(embedding_type: str):
    if embedding_type == EmbeddingType.CLASSIFICATION.value:
        if st.session_state[state.DATA_PAGE_INDEX].meta.get("title") == "Image-level Annotation Quality":
            collections, question_hash_to_collection_indexes = embedding_utils.get_collections_and_metadata(
                "cnn_classifications.csv"
            )
            identifier_to_neighbors = embedding_utils.get_identifiers_to_nearest_items(
                collections, question_hash_to_collection_indexes, int(st.session_state[state.K_NEAREST_NUM])
            )
            st.session_state[state.COLLECTIONS] = collections
            st.session_state[state.QUESTION_HASH_TO_COLLECTION_INDEXES] = question_hash_to_collection_indexes
            st.session_state[state.IDENTIFIER_TO_NEIGHBORS_CLASSES] = identifier_to_neighbors
        else:
            collections = embedding_utils.get_collections("cnn_classifications.csv")
            identifier_to_neighbors = embedding_utils.get_collections_to_neighbors(
                collections, int(st.session_state[state.K_NEAREST_NUM]), has_annotation=False
            )
            st.session_state[state.COLLECTIONS] = collections
            st.session_state[state.IDENTIFIER_TO_NEIGHBORS_CLASSES] = identifier_to_neighbors
    elif embedding_type == EmbeddingType.OBJECT.value:
        collections = embedding_utils.get_collections("cnn_objects.csv")
        identifier_to_neighbors = embedding_utils.get_collections_to_neighbors(
            collections, int(st.session_state[state.K_NEAREST_NUM])
        )
        st.session_state[state.COLLECTIONS] = collections
        st.session_state[state.IDENTIFIER_TO_NEIGHBORS_OBJECTS] = identifier_to_neighbors


def build_card(card_type: str, card_no: int, row: Series, _similarity_expanders: list[DeltaGenerator]):
    """
    Builds each sub card (the content displayed for each row in a csv file).
    """

    if card_type == EmbeddingType.CLASSIFICATION.value:
        button_name = "show similar images"
        if st.session_state[state.DATA_PAGE_INDEX].meta.get("title") == "Image-level Annotation Quality":
            image = load_or_fill_image(row)
            similarity_callback = show_similar_classification_images
        else:
            if st.session_state[state.DATA_PAGE_INDEX].meta.get("annotation_type") is None:
                image = load_or_fill_image(row)
            else:
                image = show_image_and_draw_polygons(row)
            similarity_callback = show_similar_images
    elif card_type == EmbeddingType.OBJECT.value:
        image = show_image_and_draw_polygons(row)
        button_name = "show similar objects"
        similarity_callback = show_similar_object_images
    else:
        st.write(f"{card_type} card type is not defined in EmbeddingTypes")
        return

    st.image(image)
    all_df = st.session_state[state.MERGED_DATAFRAME]
    tag_status = all_df.loc[all_df["identifier"] == row["identifier"], "tags"].item()

    multiselect_tag(row, "explorer")

    target_expander = _similarity_expanders[card_no // st.session_state[state.MAIN_VIEW_COLUMN_NUM]]

    st.button(
        str(button_name),
        key=f"similarity_button_{row['identifier']}",
        on_click=similarity_callback,
        args=(row, target_expander),
    )

    # === Write scores and link to editor === #
    tags_row = row.copy()
    index_name = st.session_state[state.DATA_PAGE_INDEX_NAME]
    if "object_class" in tags_row and not pd.isna(tags_row["object_class"]):
        tags_row["label_class_name"] = tags_row["object_class"]
        tags_row.drop("object_class")
    tags_row[index_name] = tags_row["score"]
    build_data_tags(tags_row, index_name)

    if not pd.isnull(row["description"]):
        # Hacky way for now (with incorrect rounding)
        description = re.sub(r"(\d+\.\d{0,3})\d*", r"\1", row["description"])
        st.write(f"Description: {description}")


def get_histogram(current_df: pd.DataFrame):
    # TODO: Unify with app/model_assertions/sub_pages/__init__.py:SamplesPage.get_histogram
    indexer_name = st.session_state[state.DATA_PAGE_INDEX_NAME]
    if indexer_name:
        title_suffix = f" - {indexer_name}"
    else:
        indexer_name = "Score"  # Used for plotting

    bar_chart = (
        alt.Chart(current_df, title=f"Data distribution{title_suffix}")
        .mark_bar()
        .encode(
            alt.X("score:Q", bin=alt.Bin(maxbins=100), title=indexer_name),
            alt.Y("count()", title="Num. samples"),
            tooltip=[
                alt.Tooltip("score:Q", title=indexer_name, format=",.3f", bin=True),
                alt.Tooltip("count():Q", title="Num. samples", format="d"),
            ],
        )
        .properties(height=200)
    )
    return bar_chart


def show_similar_classification_images(row: Series, expander: DeltaGenerator):
    feature_hash = row["identifier"].split("_")[-1]
    nearest_images = st.session_state[state.IDENTIFIER_TO_NEIGHBORS_CLASSES][feature_hash][row["identifier"]]

    division = 4
    column_id = 0

    for nearest_image in nearest_images:
        if column_id == 0:
            st_columns = expander.columns(division)

        image = load_or_fill_image(nearest_image["key"])

        st_columns[column_id].image(image)
        st_columns[column_id].write(f"Annotated as `{nearest_image['name']}`")
        column_id += 1
        column_id = column_id % division


def show_similar_images(row: Series, expander: DeltaGenerator):
    label_hash, data_unit_hash, frame_id, *rest = row["identifier"].split("_")
    nearest_images = st.session_state[state.IDENTIFIER_TO_NEIGHBORS_CLASSES][
        "_".join([label_hash, data_unit_hash, frame_id])
    ]

    division = 4
    column_id = 0

    for nearest_image in nearest_images:
        if column_id == 0:
            st_columns = expander.columns(division)

        image = load_or_fill_image(nearest_image["key"])

        st_columns[column_id].image(image)
        st_columns[column_id].write(f"Annotated as `{nearest_image['name']}`")
        column_id += 1
        column_id = column_id % division


def show_similar_object_images(row: Series, expander: DeltaGenerator):
    label_hash, data_unit_hash, frame_id, object_hash, *rest = row["identifier"].split("_")
    nearest_images = st.session_state[state.IDENTIFIER_TO_NEIGHBORS_OBJECTS][
        "_".join([label_hash, data_unit_hash, frame_id, object_hash])
    ]

    division = 4
    column_id = 0

    for nearest_image in nearest_images:
        if column_id == 0:
            st_columns = expander.columns(division)

        image = show_image_and_draw_polygons(nearest_image["key"])

        st_columns[column_id].image(image)
        st_columns[column_id].write(f"Annotated as `{nearest_image['name']}`")
        column_id += 1
        column_id = column_id % division


def get_unique_data_units_size(current_df: pd.DataFrame):
    data_units = set()
    identifiers = current_df["identifier"]
    for identifier in identifiers:
        key_components = identifier.split("_")
        data_units.add(key_components[0] + "_" + key_components[1])

    return len(data_units)
