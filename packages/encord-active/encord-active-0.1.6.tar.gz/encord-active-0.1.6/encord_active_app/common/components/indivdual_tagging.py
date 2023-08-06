import pandas as pd
import streamlit as st
import yaml
from pandas import Series

import encord_active_app.common.state as state


def update_image_tags(row_identifier: str, key_prefix: str):
    all_df = st.session_state[state.MERGED_DATAFRAME]
    row_no = all_df[all_df["identifier"] == row_identifier].index[0]
    all_df.at[row_no, "tags"] = st.session_state[f"{key_prefix}_multiselect_{row_identifier}"]
    # TODO this will make UI slow, make it to the DB
    all_df.to_csv(st.session_state.merged_df_filepath, index=False)


def multiselect_tag(row: Series, key_prefix: str):
    all_df = st.session_state[state.MERGED_DATAFRAME]
    tag_status = all_df.loc[all_df["identifier"] == row["identifier"], "tags"].item()
    st.multiselect(
        label="Tag image",
        options=st.session_state[state.PROJECT_TAGS],
        default=tag_status,
        key=f"{key_prefix}_multiselect_{row['identifier']}",
        label_visibility="collapsed",
        on_change=update_image_tags,
        args=(row["identifier"], key_prefix),
    )


def tag_creator():
    with st.sidebar:
        with st.form(key="tag_creator_form"):

            left, middle, right = st.columns((2, 5, 1))
            left.markdown("**Tag name:**")
            tag_name = middle.text_input("tag name", label_visibility="collapsed", key="input_text_tag")
            tag_add_button = right.form_submit_button("+")

            if tag_add_button:
                if tag_name == "":
                    st.info("Please enter a tag")
                elif tag_name in st.session_state[state.PROJECT_TAGS]:
                    st.info("Tag is already in project tags")
                else:
                    st.session_state[state.PROJECT_TAGS].append(tag_name)

        tags_sum = []
        for i, item in enumerate(st.session_state[state.PROJECT_TAGS]):
            total_tags = len([True for x in st.session_state[state.MERGED_DATAFRAME]["tags"] if item in x])
            tags_sum.append(total_tags)

        tags_dict = {"Tags": st.session_state[state.PROJECT_TAGS], "Count": tags_sum}
        st.dataframe(pd.DataFrame(tags_dict), use_container_width=True)

        # TODO fix here, write to file if there is only a change in tags
        with st.session_state[state.PROJECT_TAGS_FILE_PATH].open("w", encoding="utf-8") as f:
            project_tags = {"tags": st.session_state[state.PROJECT_TAGS]}
            f.write(yaml.dump(project_tags))
