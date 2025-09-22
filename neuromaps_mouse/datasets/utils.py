"""Functions for working with datasets."""

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
    """Get the data directory."""
    if data_dir is None:
        data_dir = os.environ.get(
            "MOUSEMAPS_DATA", str(Path.home() / "neuromaps-mouse-data")
        )
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
    if getattr(importlib.resources, "files", None) is not None:
        f_resource = importlib.resources.files("neuromaps_mouse") / relative_path
    else:
        from pkg_resources import resource_filename

        f_resource = resource_filename("neuromaps_mouse", relative_path)

    with open(f_resource) as src:
        resource_json = json.load(src)

    return resource_json


MOUSEMAPS_ATLASES = _load_resource_json("datasets/data/atlases.json")["atlases"]
MOUSEMAPS_ANNOTS = _load_resource_json("datasets/data/annotations.json")["annotations"]
MOUSEMAPS_ANNOTS_META = _load_resource_json("datasets/data/annotations-meta.json")[
    "annotations-meta"
]


def _osfify_url(osf_file_id):
    return f"https://osf.io/download/{osf_file_id}/"


def fetch_files(annotations, file_type="annotations", data_dir=None, verbose=1):
    """Fetch files from OSF."""
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
            verbose=1,
        )
        shutil.move(dl_fname, targ_fname)
        targ_fname_list.append(targ_fname)

        if verbose:
            print(f"Downloaded {targ_fname.name} to {targ_fname}")

    return targ_fname_list


def _annot_full_to_tuple(full_list):
    return [
        tuple([annot[key] for key in ["source", "desc", "space", "res"]])
        for annot in full_list
    ]


def _match_annots_by_tuple(annot_tuple_list):
    # match all then sort
    if not isinstance(annot_tuple_list, list):
        annot_tuple_list = [annot_tuple_list]
    matched = []
    for annot_tuple in annot_tuple_list:
        found = False
        for annot in MOUSEMAPS_ANNOTS:
            curr_annot_tuple = tuple(
                [annot[key] for key in ["source", "desc", "space", "res"]]
            )
            if curr_annot_tuple == annot_tuple:
                matched.append(annot)
                found = True
                break
        if not found:
            raise ValueError(f"Annotation {annot_tuple} not found in MOUSEMAPS_ANNOTS")
    return matched


def _filter_annots_by_keys(keys_dict):
    filtered = []
    for annot in MOUSEMAPS_ANNOTS:
        for key in ["source", "desc", "space", "res", "format"]:
            value = keys_dict[key]
            if value is not None and annot[key] != value:
                break
        if keys_dict["tag"] is not None and keys_dict["tag"] not in annot["tags"]:
            break
        filtered.append(annot)
    return filtered


def _check_json(osfstorage_data):
    """
    Check for errors in meta.json.

    For internal use only.

    Returns
    -------
    None
    """
    # reload the datasets and meta json files
    from rich.console import Console

    console = Console()

    MOUSEMAPS_ATLASES = _load_resource_json("datasets/data/atlases.json")["atlases"]
    MOUSEMAPS_ANNOTS = _load_resource_json("datasets/data/annotations.json")[
        "annotations"
    ]
    MOUSEMAPS_ANNOTS_META = _load_resource_json("datasets/data/annotations-meta.json")[
        "annotations-meta"
    ]

    console.print("ATLASES")
    for atlas_k, atlas_v in MOUSEMAPS_ATLASES.items():
        console.print(f"{atlas_k} >")
        for file_k, file_v in atlas_v["files"].items():
            console.print(f"  {file_k} >")
            if file_v["checksum"] == osfstorage_data[file_v["fname"]]["md5"]:
                console.print("    [bold green]✓[/bold green] checksum")
            else:
                console.print(
                    f"    [bold red]x[/bold red] checksum local: {file_v['checksum']} remote: {osfstorage_data[file_v['fname']]['md5']}"
                )

            if file_v["url"]["osf"] == osfstorage_data[file_v["fname"]]["guid"]:
                console.print("    [bold green]✓[/bold green] url")
            else:
                console.print(
                    f"    [bold red]x[/bold red] url local: {file_v['url']['osf']} remote: {osfstorage_data[file_v['fname']]['guid']}"
                )

    console.print("\nANNOTS_META")
    for annot_meta in MOUSEMAPS_ANNOTS_META:
        console.print(f"{annot_meta['source']} {annot_meta['name']} >")
        console.print("  \[annot files] >")
        for file_v in annot_meta["files"]:
            console.print(f"    {'-'.join(file_v)} >")
            try:
                matched = _match_annots_by_tuple([tuple(file_v)])
            except ValueError:
                console.print("      [bold red]x[/bold red] json")

            if len(matched) == 1:
                console.print("      [bold green]✓[/bold green] json")
            else:
                console.print("      [bold red]x[/bold red] json")

        console.print("  \[aux files] >")
        for aux_k, aux_v in annot_meta["aux_files"].items():
            console.print(f"    {aux_k} >")

            if not isinstance(aux_v, list):
                aux_v = [aux_v]
            for file_v in aux_v:
                console.print(f"      {file_v['fname']} >")
                if file_v["fname"] not in osfstorage_data:
                    console.print(
                        f"        [bold red]x[/bold red] {file_v['fname']} not found in osfstorage"
                    )
                    continue
                if file_v["checksum"] == osfstorage_data[file_v["fname"]]["md5"]:
                    console.print("        [bold green]✓[/bold green] checksum")
                else:
                    console.print(
                        f"        [bold red]x[/bold red] checksum local: {file_v['checksum']} remote: {osfstorage_data[file_v['fname']]['md5']}"
                    )
                if file_v["url"]["osf"] == osfstorage_data[file_v["fname"]]["guid"]:
                    console.print("        [bold green]✓[/bold green] url")
                else:
                    console.print(
                        f"        [bold red]x[/bold red] url local: {file_v['url']['osf']} remote: {osfstorage_data[file_v['fname']]['guid']}"
                    )

    console.print("\nANNOTS")
    for annot in MOUSEMAPS_ANNOTS:
        annotstr = "-".join(
            [annot["source"], annot["desc"], annot["space"], annot["res"]]
        )
        console.print(f"  {annotstr} >")
        if annot["fname"] not in osfstorage_data:
            console.print(f"        [bold red]x[/bold red] {annot['fname']} not found in osfstorage")
            continue
        if annot["checksum"] == osfstorage_data[annot["fname"]]["md5"]:
            console.print("    [bold green]✓[/bold green] checksum")
        else:
            console.print(
                f"    [bold red]x[/bold red] checksum local: {annot['checksum']} remote: {osfstorage_data[annot['fname']]['md5']}"
            )
        if annot["url"]["osf"] == osfstorage_data[annot["fname"]]["guid"]:
            console.print("    [bold green]✓[/bold green] url")
        else:
            console.print(
                f"    [bold red]x[/bold red] url local: {annot['url']['osf']} remote: {osfstorage_data[annot['fname']]['guid']}"
            )


def _check_osfstorage():
    """
    Check for errors in OSF links.

    For internal use only.

    Returns
    -------
    None
    """
    # reload the datasets and meta json files
    import requests
    from rich.console import Console

    console = Console()

    osfstorage_data = {}

    OSF_NODEID = "uryk3"
    OSF_URL = f"https://api.osf.io/v2/nodes/{OSF_NODEID}/files/osfstorage/"

    def _get_file_href(d):
        return d["relationships"]["files"]["links"]["related"]["href"]

    def _get_full_data(url):
        # handles pagination
        resp = requests.get(url).json()
        ret = resp["data"]
        while resp["links"].get("next"):
            href = resp["links"]["next"]
            resp = requests.get(href).json()
            ret.extend(resp["data"])
        return ret

    for kind in requests.get(OSF_URL).json()["data"]:
        kind_path = kind["attributes"]["materialized_path"]
        console.print(f"{kind_path} >")
        if kind_path == "/atlases/":
            for source in _get_full_data(_get_file_href(kind)):
                source_path = source["attributes"]["materialized_path"]
                console.print(f"  {source_path.removeprefix(kind_path)} >")
                for version in _get_full_data(_get_file_href(source)):
                    version_path = version["attributes"]["materialized_path"]
                    console.print(f"  {version_path.removeprefix(source_path)} >")
                    for file in _get_full_data(_get_file_href(version)):
                        file_path = file["attributes"]["materialized_path"]
                        console.print(f"    {file_path.removeprefix(version_path)} >")
                        console.print(f"      {file['attributes']['guid']}")
                        console.print(
                            f"      {file['attributes']['extra']['hashes']['md5']}"
                        )
                        if not file["attributes"]["guid"]:
                            requests.get(f'https://osf.io/{OSF_NODEID}/files/osfstorage{file["attributes"]["path"]}')
                        osfstorage_data[file["attributes"]["name"]] = {
                            "guid": file["attributes"]["guid"],
                            "md5": file["attributes"]["extra"]["hashes"]["md5"],
                        }
        elif kind_path == "/annotations/":
            for source in _get_full_data(_get_file_href(kind)):
                source_path = source["attributes"]["materialized_path"]
                console.print(f"  {source_path.removeprefix(kind_path)} >")
                for file in _get_full_data(_get_file_href(source)):
                    file_path = file["attributes"]["materialized_path"]
                    console.print(f"    {file_path.removeprefix(source_path)} >")
                    console.print(f"      {file['attributes']['guid']}")
                    console.print(
                        f"      {file['attributes']['extra']['hashes']['md5']}"
                    )
                    if not file["attributes"]["guid"]:
                        requests.get(f'https://osf.io/{OSF_NODEID}/files/osfstorage{file["attributes"]["path"]}')
                    osfstorage_data[file["attributes"]["name"]] = {
                        "guid": file["attributes"]["guid"],
                        "md5": file["attributes"]["extra"]["hashes"]["md5"],
                    }
        else:
            raise ValueError(f"Unknown kind_path={kind_path}")
    return osfstorage_data


# def _fill_meta_json_refs(bib_file, json_file, overwrite=False, use_defaults=False):
#     """
#     Fill in citation information for references in a JSON file.

#     For internal use only.

#     Parameters
#     ----------
#     bib_file : str
#         Path to BibTeX file containing references
#     json_file : str
#         Path to JSON file containing references
#     overwrite : bool, optional
#         Whether to overwrite existing citation information. Default: False
#     use_defaults : bool, optional
#         Whether to use default paths for `bib_file` and `json_file`. Default: False

#     Returns
#     -------
#     None
#     """
#     if use_defaults:
#         bib_file = \
#             importlib.resources.files("neuromaps") / "datasets/data/neuromaps.bib"
#         json_file = \
#             importlib.resources.files("neuromaps") / "datasets/data/meta.json"

#     from pybtex import PybtexEngine
#     engine = PybtexEngine()

#     def _get_citation(key):
#         s = engine.format_from_file(
#             filename=bib_file, style="unsrt",
#             citations=[key], output_backend="plaintext"
#             )
#         return s.strip("\n").replace("[1] ", "")

#     with open(json_file) as src:
#         nm_meta = json.load(src)

#     for entry in nm_meta["annotations"]:
#         for bib_category in ["primary", "secondary"]:
#             for bib_item in entry["refs"][bib_category]:
#                 if bib_item["bibkey"] not in ["", None]:
#                     if bib_item["citation"] == "" or overwrite:
#                         bib_item["citation"] = _get_citation(bib_item["bibkey"])

#     with open(json_file, "w") as dst:
#         json.dump(nm_meta, dst, indent=4)


def _gen_doc_listofmaps_rst(listofmaps_file):
    """
    Generate a list of maps in reStructuredText format.

    For internal use only.

    Parameters
    ----------
    listofmaps_file : str
        Path to write the list of maps

    Returns
    -------
    None
    """
    output = []

    output += [
        ".. _listofmaps:",
        "",
        "------------",
        "List of Maps",
        "------------",
        "This is a complete list of maps available in the `neuromaps_mouse` package. ",
        "\n----\n",
    ]

    for annot_meta in MOUSEMAPS_ANNOTS_META:
        title = f"{annot_meta['name']} ({annot_meta['source']})"
        output += [
            title,
            "=" * len(title),
            "",
            "**Full description**",
            "",
            f"{annot_meta['description']}",
            "",
        ]

        for file in annot_meta["files"]:
            curr_annot = _match_annots_by_tuple(tuple(file))[0]
            file_title = "-".join(file)
            key_str = ", ".join(
                [f"{k}='{curr_annot[k]}'" for k in ["source", "desc", "space", "res"]]
            )
            output += [
                file_title,
                "-" * len(file_title),
                "",
                f"**Description**: {annot_meta['file_desc'][curr_annot['desc']]}",
                "",
                f"**Format**: {curr_annot['format']}",
                "",
                "**How to use**",
                "",
                ".. code:: python",
                "",
                "    # get annotation",
                f"    fetch_annotation({key_str})",
                "",
                "    # file location",
                f"    # $MOUSEMAPS_DATA/{curr_annot['rel_path']}",
                "",
                "    # file name",
                f"    # {curr_annot['fname']}",
                "",
                "    # region mapping file",
                f"    # {curr_annot['regionmapping']}",
                "",
            ]

        output.append("**References**")
        for bib_item in annot_meta["refs"]:
            if bib_item["bibkey"] not in ["", None]:
                output += [f"    - {bib_item['citation']}"]

        output.append("\n----\n")

    output = output[:-1]

    with open(listofmaps_file, "w") as dst:
        dst.write("\n".join(output))
