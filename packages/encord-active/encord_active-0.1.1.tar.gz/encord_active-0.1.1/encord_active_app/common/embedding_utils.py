import os
import pickle
from typing import List, Optional, Tuple

import faiss
import numpy as np
import pandas as pd
import streamlit as st
from encord_active.common.utils import fix_duplicate_image_orders_in_knn_graph
from faiss import IndexFlatL2
from numpy import ndarray
from tqdm import tqdm


@st.experimental_memo(show_spinner=False)
def get_collections(embedding_name: str) -> list[dict]:

    embedding_path = st.session_state.embeddings_dir / embedding_name
    collections = []
    if os.path.isfile(embedding_path):

        with st.spinner("Reading CSV"):
            embeddings_df = pd.read_csv(embedding_path)

        txt_container = st.empty()
        txt_container.text(
            f"Building nearest neighbor graph. It should take approximately {embeddings_df.shape[0] / 1200:.0f} seconds to process embeddings."
        )
        pbar = st.progress(0.0)
        for i, item in tqdm(
            enumerate(embeddings_df.itertuples()), desc="Unpacking embeddings", total=len(embeddings_df)
        ):
            tmp_entry = eval(item.description)
            tmp_entry["embedding"] = np.array(
                [float(x) for x in item.embedding[1:-1].replace(" ", "").split(",")],
                dtype=np.float32,
            )
            tmp_entry["name"] = item.object_class
            collections.append(tmp_entry)
            if i % 1200 == 1199 or i == embeddings_df.shape[0]:
                pbar.progress((i + 1) / embeddings_df.shape[0])
        txt_container.empty()
        pbar.empty()
    else:
        collections = []

    return collections


@st.experimental_memo
def get_collections_and_metadata(embedding_name: str) -> Tuple[list[dict], dict]:
    try:
        collections = get_collections(embedding_name)

        embedding_metadata_file_name = "embedding_classifications_metadata.pkl"
        embedding_metadata_path = st.session_state.embeddings_dir / embedding_metadata_file_name
        if os.path.isfile(embedding_metadata_path):
            with open(embedding_metadata_path, "rb") as f:
                question_hash_to_collection_indexes_local = pickle.load(f)
        else:
            question_hash_to_collection_indexes_local = {}

        return collections, question_hash_to_collection_indexes_local
    except Exception as e:
        print(str(e))
        return [], {}


def get_key_from_index(collection: dict, question_hash: Optional[str] = None, has_annotation=True) -> str:
    label_hash = collection["label_row"]
    du_hash = collection["data_unit"]
    frame_idx = int(collection["frame"])

    if not has_annotation:
        key = f"{label_hash}_{du_hash}_{frame_idx:05d}"
    else:
        if question_hash:
            key = f"{label_hash}_{du_hash}_{frame_idx:05d}_{question_hash}"
        else:
            object_hash = collection["objectHash"]
            key = f"{label_hash}_{du_hash}_{frame_idx:05d}_{object_hash}"

    return key


def get_identifier_to_neighbors(
    collections: list[dict], nearest_indexes: np.ndarray, has_annotation=True
) -> dict[str, list]:
    nearest_neighbors = {}
    n, k = nearest_indexes.shape
    for i in range(n):
        key = get_key_from_index(collections[i], has_annotation=has_annotation)
        temp_list = []
        for j in range(1, k):
            temp_list.append(
                {
                    "key": get_key_from_index(collections[nearest_indexes[i, j]], has_annotation=has_annotation),
                    "name": collections[nearest_indexes[i, j]]["name"],
                }
            )
        nearest_neighbors[key] = temp_list
    return nearest_neighbors


def convert_to_index(collections: list[dict]) -> tuple[ndarray, IndexFlatL2]:
    embeddings_list: List[list] = [x["embedding"] for x in collections]
    embeddings = np.array(embeddings_list).astype(np.float32)

    db_index = faiss.IndexFlatL2(embeddings.shape[1])
    db_index.add(embeddings)  # pylint: disable=no-value-for-parameter
    return embeddings, db_index


def convert_to_indexes(collections, question_hash_to_collection_indexes):
    embedding_databases, indexes = {}, {}

    for question_hash in question_hash_to_collection_indexes:
        selected_collections = [collections[i] for i in question_hash_to_collection_indexes[question_hash]]

        if len(selected_collections) > 10:
            embedding_database = np.stack(list(map(lambda x: x["embedding"], selected_collections)))

            index = faiss.IndexFlatL2(embedding_database.shape[1])
            index.add(embedding_database)  # pylint: disable=no-value-for-parameter

            embedding_databases[question_hash] = embedding_database
            indexes[question_hash] = index

    return embedding_databases, indexes


@st.experimental_memo
def get_identifiers_to_nearest_items(
    _collections: list[dict], question_hash_to_collection_indexes: dict[str, list], k: int
):
    k = k + 1
    nearest_indexes = {}
    embedding_databases, indexes = convert_to_indexes(_collections, question_hash_to_collection_indexes)
    for question_hash in question_hash_to_collection_indexes:
        if len(question_hash_to_collection_indexes[question_hash]) > 10:
            nearest_distance, nearest_index = indexes[question_hash].search(  # pylint: disable=no-value-for-parameter
                embedding_databases[question_hash], k
            )
            nearest_index = fix_duplicate_image_orders_in_knn_graph(nearest_index)
            nearest_neighbors = {}
            n, k = nearest_index.shape
            for i in range(n):
                target_collection_index = question_hash_to_collection_indexes[question_hash][i]
                key = get_key_from_index(_collections[target_collection_index], question_hash)
                temp_list = []
                for j in range(1, k):
                    collection_index = question_hash_to_collection_indexes[question_hash][nearest_index[i, j]]
                    temp_list.append(
                        {
                            "key": get_key_from_index(_collections[collection_index], question_hash),
                            "name": _collections[collection_index]["classification_answers"][question_hash][
                                "answer_name"
                            ],
                        }
                    )
                nearest_neighbors[key] = temp_list
            nearest_indexes[question_hash] = nearest_neighbors

    return nearest_indexes


@st.experimental_memo
def get_collections_to_neighbors(_collections: list[dict], k: int, has_annotation=True) -> dict[str, list]:
    # from collections build faiss index
    embedding_database, index = convert_to_index(_collections)
    k = k + 1

    # TODO_l Check proper usage of index.search()
    nearest_distances, nearest_indexes = index.search(embedding_database, k)  # pylint: disable=no-value-for-parameter

    return get_identifier_to_neighbors(_collections, nearest_indexes, has_annotation)
