import json
import logging
import os
from concurrent.futures import ThreadPoolExecutor as Executor
from concurrent.futures import as_completed
from dataclasses import dataclass
from functools import partial
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union

import encord.exceptions
import requests
from encord import Project
from encord.orm.label_row import LabelRow
from encord_active.common.utils import slice_video_into_frames
from tqdm import tqdm

logger = logging.getLogger(__name__)
encord_logger = logging.getLogger("encord")
encord_logger.setLevel(logging.ERROR)
_DATA_CACHE_DIR = Path("../../data/label_rows")


@dataclass
class DataSpecs:
    img: Path
    du: dict
    lr: dict


def collect_async(fn, job_args, key_fn, max_workers=min(os.cpu_count(), 10), **kwargs):
    """
    Distribute work across multiple workers. Good for, e.g., downloading data.
    Will return results in dictionary.
    :param fn: The function to be applied
    :param job_args: Arguments to `fn`.
    :param key_fn: Function to determine dictionary key for the result (given the same input as `fn`).
    :param max_workers: Number of workers to distribute work over.
    :param kwargs: Arguments passed on to tqdm.
    :return: Dictionary {key_fn(*job_args): fn(*job_args)}
    """
    job_args = list(job_args)
    if not isinstance(job_args[0], tuple):
        job_args = [(j,) for j in job_args]

    results = {}
    with tqdm(total=len(job_args), **kwargs) as pbar:
        with Executor(max_workers=max_workers) as exe:
            jobs = {exe.submit(fn, *args): key_fn(*args) for args in job_args}
            for job in as_completed(jobs):
                key = jobs[job]

                result = job.result()
                if result:
                    results[key] = result

                pbar.update(1)
    return results


def download_file(
    url: str,
    destination: Path,
    byte_size=1024,
):
    if destination.is_file():
        return destination

    r = requests.get(url, stream=True)
    with destination.open("wb") as f:
        for chunk in r.iter_content(chunk_size=byte_size):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)
                f.flush()

    return destination


def get_label_row(lr, client, cache_dir, refresh=False) -> Optional[LabelRow]:
    if isinstance(cache_dir, str):
        cache_dir = Path(cache_dir)

    if not lr.label_hash:
        return None

    cache_pth = cache_dir / "data" / lr.label_hash / "label_row.json"

    if not refresh and cache_pth.is_file():
        # Load cached version
        try:
            with cache_pth.open("r") as f:
                return LabelRow(json.load(f))
        except json.decoder.JSONDecodeError:
            pass

    try:
        lr = client.get_label_row(lr.label_hash)
    except encord.exceptions.UnknownException as e:
        logger.warning(
            f"Failed to download label row with label_hash {lr.label_hash[:8]}... and data_title {lr.data_title}"
        )
        return None

    # Cache label row.
    cache_pth.parent.mkdir(parents=True, exist_ok=True)
    with cache_pth.open("w") as f:
        json.dump(lr, f, indent=2)

    return lr


def download_all_label_rows(client, subset_size: int = -1, **kwargs) -> Dict[str, LabelRow]:
    label_rows = client.list_label_rows()
    if subset_size > 0:
        label_rows = label_rows[:subset_size]

    return collect_async(
        partial(get_label_row, client=client, **kwargs),
        label_rows,
        lambda lr: lr.label_hash,
        desc="Collecting label rows from Encord SDK.",
    )


def download_images_from_data_unit(lr, cache_dir, **kwargs) -> Optional[List[Path]]:
    if isinstance(cache_dir, str):
        cache_dir = Path(cache_dir)

    label_hash = lr.label_hash

    if label_hash is None:
        return None

    label_pth = cache_dir / "data" / label_hash
    label_pth.mkdir(parents=True, exist_ok=True)

    lr_path = label_pth / "label_row.json"
    if not lr_path.exists():
        with (label_pth / "label_row.json").open("w") as f:
            json.dump(lr, f, indent=2)

    frame_pth = label_pth / "images"

    frame_pth.mkdir(parents=True, exist_ok=True)
    frame_pths: List[Path] = []
    data_units = sorted(lr.data_units.values(), key=lambda du: int(du["data_sequence"]))
    for du in data_units:
        suffix = f".{du['data_type'].split('/')[1]}"
        out_pth = (frame_pth / du["data_hash"]).with_suffix(suffix)
        download_file(du["data_link"], out_pth)
        frame_pths.append(out_pth)

    # if label row's data type is video then extract frames
    if lr.data_type == "video":
        video_path = frame_pths[0]
        frame_pths.clear()
        for out_pth in slice_video_into_frames(video_path)[0].values():
            frame_pths.append(out_pth)

    return frame_pths


def download_all_images(label_rows, cache_dir: Union[str, Path], **kwargs) -> Dict[str, List[Path]]:
    return collect_async(
        partial(download_images_from_data_unit, cache_dir=cache_dir, **kwargs),
        label_rows.values(),
        lambda lr: lr.label_hash,
        desc="Collecting frames from label rows.",
    )


def prepare_data(
    project: Project, cache_dir: Path, use_images: bool = False, subset_size: int = -1, **kwargs
) -> Tuple[Dict[str, LabelRow], Optional[Dict[str, List[Path]]]]:
    label_rows = download_all_label_rows(project, subset_size=subset_size, cache_dir=cache_dir, **kwargs)

    image_paths = None
    if use_images:
        image_paths = download_all_images(label_rows, cache_dir=cache_dir, **kwargs)

    return label_rows, image_paths
