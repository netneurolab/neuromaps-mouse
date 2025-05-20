"""Functions for loading and remapping data."""

import numpy as np
import pandas as pd

from neuromaps_mouse.datasets.utils import get_data_dir
from neuromaps_mouse.datasets.annotations import _match_annots_by_tuple


def load_nifti():
    pass


def load_image_data():
    pass


def _remap_region_data(
    original_values, value_format, regionmapping, target_column, hemi=None
):
    if hemi is not None:
        if hemi not in ["left", "right"]:
            raise ValueError(
                f"Invalid hemi value: {hemi}. Should be one of ['left', 'right']"
            )
        regionmapping = regionmapping[regionmapping["hemi"] == hemi]
        indices_hemi = regionmapping.index.tolist()
        regionmapping = regionmapping.reset_index(drop=True)
        if value_format == "matrix":
            original_values = original_values[np.ix_(indices_hemi, indices_hemi)]
        else:
            original_values = original_values[indices_hemi, :]

    # drop not-mapped regions
    has_null = regionmapping[target_column].isnull().any()

    # remove the null values
    if has_null:
        regionmapping_nona = regionmapping.dropna(subset=target_column, axis=0)
        indices_nona = regionmapping_nona.index.tolist()
        regionmapping_nona = regionmapping_nona.reset_index(drop=True)
        if value_format == "matrix":
            original_values_nona = original_values[np.ix_(indices_nona, indices_nona)]
        else:
            original_values_nona = original_values[indices_nona, :]
    else:
        regionmapping_nona = regionmapping
        original_values_nona = original_values

    # average the duplicate regions
    has_duplicated = regionmapping_nona[target_column].duplicated().any()

    if has_duplicated:
        if value_format == "matrix":
            raise ValueError(
                "Duplicated regions in regionmapping, but annotation format is matrix"
            )
        indices_dup = (
            regionmapping_nona.groupby(target_column)
            .apply(lambda x: x.index.tolist())
            .tolist()
        )
        original_values_nona_dedup = np.array(
            [
                np.mean(original_values_nona[indices, :], axis=0)
                for indices in indices_dup
            ]
        )
        regions_nona_dedup = list(
            regionmapping_nona.groupby(target_column).groups.keys()
        )
    else:
        regions_nona_dedup = regionmapping_nona[target_column].tolist()
        original_values_nona_dedup = original_values_nona

    return original_values_nona_dedup, regions_nona_dedup


def load_region_data(
    annotation, return_original=False, remap_kws=None, data_dir=None, verbose=1
):
    if annotation[-1] != "region":
        raise ValueError(f"Annotation {annotation} is not a region annotation")

    data_dir = get_data_dir(data_dir=data_dir)

    annotation_full = _match_annots_by_tuple(annotation)[0]

    # TODO check if the file exists, if not, download it

    original_values_path = (
        data_dir
        / "annotations"
        / annotation_full["rel_path"]
        / annotation_full["fname"]
    )
    regionmapping_path = (
        data_dir
        / "annotations"
        / annotation_full["rel_path"]
        / annotation_full["regionmapping"]
    )

    # original_values = np.loadtxt(
    #     data_dir
    #     / "annotations"
    #     / annotation_full["rel_path"]
    #     / annotation_full["fname"],
    #     delimiter=",",
    # )
    regionmapping = pd.read_csv(regionmapping_path)

    if annotation_full["format"] == "scalar":
        original_values = np.loadtxt(original_values_path, delimiter=",")[:, np.newaxis]
        assert original_values.shape == (len(regionmapping), 1)
    elif annotation_full["format"] == "tabular":
        original_values = pd.read_csv(original_values_path, header=0)
        tabular_header = original_values.columns.tolist()
        original_values = original_values.to_numpy()
        assert original_values.shape[0] == len(regionmapping)
    elif annotation_full["format"] == "matrix":
        assert (
            original_values.shape[0] == original_values.shape[1] == len(regionmapping)
        )

    if return_original:
        if annotation_full["format"] == "tabular":
            return (
                original_values,
                regionmapping["original_region"].tolist(),
                tabular_header,
            )
        else:
            return original_values, regionmapping["original_region"].tolist()

    remap_dict = remap_kws or {}

    original_values_nona_dedup, region_nona_dedup = _remap_region_data(
        original_values,
        annotation_full["format"],
        regionmapping,
        "allenccfv3_acronym",
        **remap_dict,
    )

    if annotation_full["format"] == "tabular":
        return original_values_nona_dedup, region_nona_dedup, tabular_header
    else:
        return original_values_nona_dedup, region_nona_dedup
