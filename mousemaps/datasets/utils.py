
import os
import json
import shutil
import importlib.resources
from pathlib import Path

try:
    # nilearn 0.10.3
    from nilearn.datasets._utils import fetch_single_file as _fetch_file, _md5_sum_file
except ImportError:
    from nilearn.datasets.utils import _fetch_file, _md5_sum_file


def get_data_dir(data_dir=None):
    if data_dir is None:
        data_dir = os.environ.get('MOUSEMAPS_DATA', str(Path.home() / 'mousemaps-data'))
    data_dir = Path(data_dir).expanduser()
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir


def _load_resource_json(relative_path):
    """
    Load JSON file from package resources.

    Parameters
    ----------
    relative_path : str
        Path to JSON file relative to package resources

    Returns
    -------
    resource_json : dict
        JSON file loaded as a dictionary
    """
    # handling pkg_resources.resource_filename deprecation
    if getattr(importlib.resources, 'files', None) is not None:
        f_resource = importlib.resources.files("mousemaps") / relative_path
    else:
        from pkg_resources import resource_filename
        f_resource = resource_filename('mousemaps', relative_path)

    with open(f_resource) as src:
        resource_json = json.load(src)

    return resource_json


MOUSEMAPS_ATLASES = _load_resource_json(
    "datasets/data/atlases.json")["atlases"]
MOUSEMAPS_ANNOTS = _load_resource_json(
    "datasets/data/annotations.json")["annotations"]
MOUSEMAPS_ANNOTS_META = _load_resource_json(
    "datasets/data/annotations-meta.json")["annotations-meta"]


def _osfify_url(osf_file_id):
    return f"https://osf.io/download/{osf_file_id}/"


def fetch_files(annotations, file_type="annotations", data_dir=None, verbose=1):
    targ_fname_list = []
    for annot in annotations:
        if file_type in ["annotations", "annotations-meta"]:
            targ_path = Path(data_dir) / "annotations"
        elif file_type == "atlases":
            targ_path = Path(data_dir) / "atlases"
        else:
            raise ValueError(f"Unknown file_type={file_type}")

        targ_fname = targ_path / annot["rel_path"] / annot["fname"]
        if targ_fname.exists():
            if _md5_sum_file(targ_fname) == annot["checksum"]:
                targ_fname_list.append(targ_fname)
                if verbose:
                    print(f"Found {targ_fname.name} at {targ_fname}")
                continue
            else:
                if verbose:
                    print(f"Checksum mismatch for {targ_fname.name}, redownloading...")

        dl_fname = _fetch_file(
            _osfify_url(annot["url"]["osf"]),
            targ_fname.parent,
            resume=True,
            md5sum=annot["checksum"],
            verbose=1
        )
        shutil.move(dl_fname, targ_fname)
        targ_fname_list.append(targ_fname)

        if verbose:
            print(f"Downloaded {targ_fname.name} to {targ_fname}")

    return targ_fname_list
