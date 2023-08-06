from pathlib import Path

import streamlit as st

from encord_active_app.common.utils import set_page_config, setup_page


def getting_started():
    setup_page()

    logo_pth = Path(__file__).parents[1] / "assets" / "encord_2_02.png"
    _, col, _ = st.columns([4, 2, 4])  # Hack to center and scale content
    with col:
        st.image(logo_pth.as_posix())

    _, col, _ = st.columns([2, 6, 2])
    with col:
        st.video("https://youtu.be/i6xHOy3CcCY")
        st.markdown(
            """
    ### Our [Documentation](https://encord-active-docs.web.app/) contains everything there is to know about Encord Active
    """
        )

    st.markdown(
        """**Encord Active** is an open-source Python library that enables users to get insights about their
Machine Learning components (Data, Labels, and Models) and actionable results. With Encord Active, you

* Build high quality dataset
* Get better annotations
* Build more robust models

This page will provide information on how to use it and some frequently used concepts.."""
    )

    st.header("Concepts")
    st.markdown(
        """
**Index:** Indexes are the backbone of the Encord Active. An index gives a value to each actionable item in the project.
Some indexes only give information about the data without not meaning any quality (e.g: level of contrast, red density),
 meanwhile, some indexes define quality (e.g: Annotation quality).
"""
    )

    st.header("Label Quality")
    st.markdown(
        """
In the **Label Quality** page, summary and available indexes for your project are listed.
In the **Summary**, you will find outliers related to available indexes.
In available **Indexes** you will find two different groups of indexes ending with (F) and (O).
- Indexes ending with (F) refers to frame-level indexes. These indexes only evaluates frame-level information without \
using any label.
- Indexes ending with (O) refers to object-level indexes. These indexes utilize annotations.

Indexes can be filtered according to the classes and annotators if they are available for that index.

"""
    )

    st.header("Model Assertions")
    st.markdown(
        """
In the Model Assertions page, you will find five different pages:

### 1. Metrics

#### Index importance
Gives information on which indexes have more influence on the model performance.

#### Subset selection scores
Average Precision (AP) and Average Recall (AR) values for the selected classes are provided along with \
Precision-Recall curve.

### 2. Performance by Indexer
This is where indexes come into play. This page basically shows performance of the model as a function of the \
selected index. Indexes can be chosen in the left sidebar. You can visualise index values where the model is under \
performing. In other words, you can get your model's failure modes.

### 3. True Positives
These are the predictions for which the IOU was sufficiently high and the confidence score was the highest amongst \
predictions that overlap with the label.

### 4. False Positives
These are the predictions for which either of the following is true:

- The IOU between the prediction and the best matching label was too low
- There was another prediction with higher model confidence which matched the label already
- The predicted class didn't match

### 5. False Negatives
These are the labels that were not matched with any predictions.

"""
    )


if __name__ == "__main__":
    set_page_config()
    getting_started()
