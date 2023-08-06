import os
import shutil
from pathlib import Path
from typing import Any, Collection, Dict, List, Optional, Tuple

import av
import cv2
import numpy as np
import yaml
from encord import EncordUserClient, Project
from loguru import logger
from shapely.geometry import Polygon
from tqdm import tqdm


def fetch_project_info(data_dir: Path) -> Project:
    meta_file = data_dir / "project_meta.yaml"
    if not meta_file.is_file():
        logger.error("Couldn't find meta file for project")

    with meta_file.open("r", encoding="utf-8") as f:
        project_meta = yaml.safe_load(f)

    # == Key file == #
    if "ssh_key_path" not in project_meta:
        raise ValueError("SSH Key path missing in project metadata.")

    private_key_file = Path(project_meta["ssh_key_path"]).expanduser().absolute()
    with private_key_file.open("r", encoding="utf-8") as f:
        private_key = f.read()
    client = EncordUserClient.create_with_ssh_private_key(private_key)

    # == Project hash == #
    if "project_hash" not in project_meta:
        raise ValueError("Project ID is missing in project metadata.")
    project_hash = project_meta["project_hash"]
    project = client.get_project(project_hash=project_hash)
    return project


def get_du_size(data_unit, img_pth):
    if "width" not in data_unit.keys() or "height" not in data_unit.keys():
        image = cv2.imread(img_pth.as_posix())
        img_h, img_w = image.shape[:2]
    else:
        img_w = int(data_unit["width"])
        img_h = int(data_unit["height"])
    return img_h, img_w


def get_object_coordinates(o: dict) -> Optional[list[tuple[Any, Any]]]:
    """
    Convert Encord object dict into list of coordinates.
    :param o: the Encord object dict.
    :return: the list of coordinates.
    """
    if o["shape"] in ["polygon", "polyline", "point", "skeleton"]:
        points_dict = o[o["shape"]]
        points = [(points_dict[str(i)]["x"], points_dict[str(i)]["y"]) for i in range(len(points_dict))]
    elif o["shape"] == "bounding_box":
        bbox = o["boundingBox"]
        points = [
            (bbox["x"], bbox["y"]),
            (bbox["x"] + bbox["w"], bbox["y"]),
            (bbox["x"] + bbox["w"], bbox["y"] + bbox["h"]),
            (bbox["x"], bbox["y"] + bbox["h"]),
        ]
    else:
        logger.warning(f"Unknown shape {o['shape']} in get_object_coordinates function")
        return None

    return points


def get_polygon(o: dict) -> Optional[Polygon]:
    """
    Convert object dict into shapely polygon.
    :param o: the Encord object dict.
    :return: The polygon object.
    """
    if o["shape"] in ["bounding_box", "polygon"]:
        points = get_object_coordinates(o)
    else:
        logger.warning(f"Unknown shape {o['shape']} in get_polygon function")
        return None

    if points is None or len(points) < 3:
        logger.debug("Less than 3 points")
        return None

    polygon = Polygon(points)
    if not polygon.is_simple:
        logger.debug("Not simple")
        return None

    return polygon


def get_geometry_from_encord_object(obj: dict, w: int, h: int) -> Optional[np.ndarray]:
    """
    Convert Encord object dictionary to polygon coordinates used to draw geometries
    with opencv.
    :param obj: the encord object dict
    :param w: the image width
    :param h: the image height
    :return: The polygon coordinates
    """

    polygon = get_polygon(obj)
    if polygon:
        img_size = np.array([[w, h]])
        return (np.array(polygon.exterior.xy).T * img_size).astype(int)
    else:
        return None


def get_iou(p1: Polygon, p2: Polygon):
    """
    Compute IOU between two polygons. If polygons are invalid, 0 will be returned.
    :param p1: polygon 1
    :param p2: polygon 2
    :return: the IOU.
    """
    try:
        intersect = p1.intersection(p2).area
        union = p1.union(p2).area
        return intersect / union
    except:
        return 0


def slice_video_into_frames(
    video_path: Path, out_dir: Path = None, wanted_frames: Collection[int] = None
) -> Tuple[Dict[int, Path], List[int]]:
    frames_dir = out_dir if out_dir else video_path.parent
    frames_dir_existed = frames_dir.exists()

    sliced_frames: Dict[int, Path] = {}
    dropped_frames: List[int] = []

    if frames_dir_existed:
        frames = {
            int(p.stem.rsplit("_", 1)[-1].split(".", 1)[0]): p for p in frames_dir.iterdir() if p.suffix == ".png"
        }
        if frames:
            return frames, []

    try:
        frames_dir.mkdir(parents=True, exist_ok=True)

        video_name = video_path.stem

        with av.open(str(video_path), mode="r") as container:
            for frame in tqdm(
                container.decode(video=0),
                desc="Extracting frames from video",
                leave=True,
                total=container.streams.video[0].frames,
            ):
                frame_num = frame.index

                if wanted_frames is None or frame_num in wanted_frames:

                    if not frame.is_corrupt:
                        frame_name = f"{video_name}_{frame_num}.png"

                        frame_path = Path(frames_dir, frame_name)
                        frame.to_image().save(frame_path)

                        sliced_frames[frame_num] = frame_path
                    else:
                        dropped_frames.append(frame_num)

            return sliced_frames, dropped_frames
    except Exception:
        if not frames_dir_existed:
            shutil.rmtree(frames_dir)
        else:
            for _, frame_path in sliced_frames.items():
                delete_locally_cached_file(frame_path)
        raise


def delete_locally_cached_file(file_path) -> None:
    """
    Deleted cached file from local storage
    :param file_path: str with local file path
    """
    try:
        os.remove(file_path)
    except Exception:
        logger.exception(f"Failed to remove local file [{file_path}]")


def get_bbox_from_encord_label_object(obj: dict, w: int, h: int) -> Optional[tuple]:
    transformed_obj = get_geometry_from_encord_object(obj, w, h)
    if transformed_obj is not None:
        return cv2.boundingRect(transformed_obj)
    else:
        logger.debug("Detected invalid polygon (self-crossing or less than 3 vertices).")
        return None


def fix_duplicate_image_orders_in_knn_graph(nearest_indexes: np.ndarray) -> np.ndarray:
    """
    Duplicate images create problem in nearest neighbor order, for example for index 6 its closest
    neighbors can be [5,6,1,9,3] if 5 and 6 is duplicate, it should be [6,5,1,9,3]. This function ensures that
    the first item is the queried index.

    :param nearest_indexes: nearest indexes obtained from search method of faiss index
    :return: fixed nearest indexes
    """
    for i, row in enumerate(nearest_indexes):
        if i != row[0]:
            target_index = np.where(row == i)
            if len(target_index[0]) == 0:
                row[0] = i
            else:
                row[0], row[target_index[0][0]] = row[target_index[0][0]], row[0]

    return nearest_indexes
