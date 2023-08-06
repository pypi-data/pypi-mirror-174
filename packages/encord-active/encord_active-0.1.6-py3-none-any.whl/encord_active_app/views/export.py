from datetime import datetime
from typing import Tuple, cast

import pandas as pd
import streamlit as st
import streamlit_modal as modal
from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
)

import encord_active_app.common.state as state
from encord_active_app.common.utils import load_merged_df, set_page_config, setup_page


def filter_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds a UI on top of a dataframe to let apps filter columns

    Args:
        df (pd.DataFrame): Original dataframe

    Returns:
        pd.DataFrame: Filtered dataframe
    """
    modify = st.checkbox("Add filters")

    if not modify:
        return df

    df = df.copy()

    # Try to convert datetimes into a standard format (datetime, no timezone)
    for col in df.columns:
        if is_object_dtype(df[col]):
            try:
                df[col] = pd.to_datetime(df[col])
            except Exception:
                pass

        if is_datetime64_any_dtype(df[col]):
            df[col] = df[col].dt.tz_localize(None)

    modification_container = st.container()

    with modification_container:
        to_filter_columns = st.multiselect("Filter dataframe on", df.columns)
        for column in to_filter_columns:
            left, right = st.columns((1, 20))
            left.write("↳")

            if column == "tags":
                tag_filters = right.multiselect("Choose tags to filter", options=st.session_state[state.PROJECT_TAGS])
                filtered_rows = [True if set(tag_filters) <= set(x) else False for x in df["tags"]]
                df = df.loc[filtered_rows]

            # Treat columns with < 10 unique values as categorical
            elif is_categorical_dtype(df[column]) or df[column].nunique() < 10:
                if df[column].isnull().sum() != df.shape[0]:
                    user_cat_input = right.multiselect(
                        f"Values for {column}",
                        df[column].unique(),
                        default=list(df[column].unique()),
                    )
                    df = df[df[column].isin(user_cat_input)]
                else:
                    right.markdown(f"For column *{column}*, all values are NaN")
            elif is_numeric_dtype(df[column]):
                _min = float(df[column].min())
                _max = float(df[column].max())
                step = (_max - _min) / 100
                user_num_input = right.slider(
                    f"Values for {column}",
                    min_value=_min,
                    max_value=_max,
                    value=(_min, _max),
                    step=step,
                )
                df = df[df[column].between(*user_num_input)]
            elif is_datetime64_any_dtype(df[column]):
                first = df[column].min()
                last = df[column].max()
                res = right.date_input(
                    f"Values for {column}",
                    min_value=first,
                    max_value=last,
                    value=(first, last),
                )
                if isinstance(res, tuple) and len(res) == 2:
                    res = cast(Tuple[pd.Timestamp, pd.Timestamp], map(pd.to_datetime, res))  # type: ignore
                    start_date, end_date = res
                    df = df.loc[df[column].between(start_date, end_date)]
            else:
                user_text_input = right.text_input(
                    f"Substring or regex in {column}",
                )
                if user_text_input:
                    df = df[df[column].astype(str).str.contains(user_text_input)]

    return df


def export():
    load_merged_df()
    filtered_df = filter_dataframe(st.session_state[state.MERGED_DATAFRAME].copy())
    st.markdown(f"**Total row:** {filtered_df.shape[0]}")
    st.dataframe(filtered_df)

    action_columns = st.columns((5, 2, 2, 2))
    action_columns[0].download_button(
        "⬇ Download filtered data",
        filtered_df.to_csv(index=False).encode("utf-8"),
        file_name=f"Encord Active Data {datetime.now().strftime('%Y_%m_%d %H_%M_%S')}.csv",
    )
    delete_btn = action_columns[1].button("❌ Delete")
    edit_btn = action_columns[2].button("🖋 Edit")
    augment_btn = action_columns[3].button("➕ Augment")

    if delete_btn or edit_btn or augment_btn:
        modal.open()

    if modal.is_open():
        with modal.container():
            st.markdown(
                '<h2 style="text-align: center;"> Please contact <a href="https://encord.com/request_demo">Encord</a></h2>.',
                unsafe_allow_html=True,
            )


if __name__ == "__main__":
    set_page_config()
    setup_page()
    export()
