"""Functions for annotation data fetching and loading."""

from neuromaps_mouse.datasets.utils import (
    MOUSEMAPS_ANNOTS,
    MOUSEMAPS_ANNOTS_META,
    get_data_dir,
    fetch_files,
    _annot_full_to_tuple,
    _filter_annots_by_keys,
    _match_annots_by_tuple
)


def get_annotation_dir(data_dir=None):
    data_dir = get_data_dir(data_dir=data_dir)
    return data_dir / "annotations"


def available_annotations(
    source=None, desc=None, space=None, res=None, tag=None, format=None
):
    if source == "all":
        return _annot_full_to_tuple(MOUSEMAPS_ANNOTS)
    else:
        return _annot_full_to_tuple(_filter_annots_by_keys(locals()))


def fetch_annotation(annotations, data_dir=None, return_single=False, verbose=1):
    data_dir = get_data_dir(data_dir=data_dir)

    if not isinstance(annotations, list):
        annotations = [annotations]
    annotations_full = _match_annots_by_tuple(annotations)

    targ_fname_list = fetch_files(
        annotations_full, file_type="annotations", data_dir=data_dir, verbose=verbose
    )

    # also download the related aux files, regionmapping, for now
    source_list = list(set([annot["source"] for annot in annotations_full]))

    if verbose:
        print(f"Downloading regionmapping files for {source_list}")
    targ_annot_meta_fname_list = _fetch_annotation_meta_files(
        list(set([annot["source"] for annot in annotations_full])),
        which="regionmapping",
        data_dir=data_dir,
        verbose=verbose,
    )

    if len(annotations_full) == 1 and return_single:
        return annotations[0], targ_fname_list[0]
    else:
        return annotations, targ_fname_list


def _fetch_annotation_meta_files(
    sources, which="regionmapping", data_dir=None, verbose=1
):
    data_dir = get_data_dir(data_dir=data_dir)

    if not isinstance(sources, list):
        sources = [sources]

    filtered_annot_meta_list = [
        annot_meta["aux_files"][which]
        for annot_meta in MOUSEMAPS_ANNOTS_META
        if annot_meta["source"] in sources
    ]
    filtered_annot_meta_list = [
        item
        for sublist in filtered_annot_meta_list
        for item in (
            sublist if isinstance(sublist, list) else [sublist]
        )
    ]

    targ_fname_list = fetch_files(
        filtered_annot_meta_list,
        file_type="annotations-meta",
        data_dir=data_dir,
        verbose=verbose,
    )

    return targ_fname_list
