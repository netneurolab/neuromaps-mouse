"""Atlas data fetching and loading functions."""

from mousemaps.datasets.utils import (
    MOUSEMAPS_ATLASES,
    fetch_files,
    get_data_dir
)

def get_atlas_dir(data_dir=None):
    data_dir = get_data_dir(data_dir=data_dir)
    return data_dir / "atlases"

def fetch_allenccfv3(which=None, return_single=True, data_dir=None, verbose=1):
    data_dir = get_data_dir(data_dir=data_dir)
    atlas = MOUSEMAPS_ATLASES["allen-ccfv3"]

    available_files = list(atlas["files"].keys())

    if which is None or which == "all":
        which = list(available_files)

    if not isinstance(which, list):
        which = [which]

    atlas_files = []
    for w in which:
        if w is None or w not in available_files:
            raise ValueError(
                f"Invalid 'which' value: {w}. " f"Should be one of {available_files}"
            )
        atlas_files.append(atlas["files"][w])

    targ_fname_list = fetch_files(
        atlas_files, file_type="atlases", data_dir=data_dir, verbose=verbose
    )

    if len(targ_fname_list) == 1 and return_single:
        return targ_fname_list[0]
    else:
        return targ_fname_list


def fetch_all_atlases():
    pass
