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


def _check_json(osfstorage_data, overwrite=False):
    """
    Check for errors in meta.json.

    For internal use only.

    Returns
    -------
    None
    """
    # reload the datasets and meta json files
    from rich.console import Console
    import importlib.resources

    console = Console()

    # Load JSON files
    MOUSEMAPS_ATLASES = _load_resource_json("datasets/data/atlases.json")["atlases"]
    MOUSEMAPS_ANNOTS = _load_resource_json("datasets/data/annotations.json")[
        "annotations"
    ]
    MOUSEMAPS_ANNOTS_META = _load_resource_json("datasets/data/annotations-meta.json")[
        "annotations-meta"
    ]

    # Track if any changes were made
    atlases_updated = False
    annots_updated = False
    annots_meta_updated = False

    console.print("ATLASES")
    for atlas_k, atlas_v in MOUSEMAPS_ATLASES.items():
        console.print(f"{atlas_k} >")
        for file_k, file_v in atlas_v["files"].items():
            console.print(f"  {file_k} >")
            if file_v["checksum"] == osfstorage_data[file_v["fname"]]["md5"]:
                console.print("    [bold green]✓[/bold green] checksum")
            else:
                if overwrite:
                    file_v["checksum"] = osfstorage_data[file_v["fname"]]["md5"]
                    atlases_updated = True
                    console.print("    [bold yellow]↻[/bold yellow] checksum updated")
                else:
                    console.print(
                        f"    [bold red]x[/bold red] "
                        f"checksum local: {file_v['checksum']} "
                        f"remote: {osfstorage_data[file_v['fname']]['md5']}"
                    )

            if file_v["url"]["osf"] == osfstorage_data[file_v["fname"]]["guid"]:
                console.print("    [bold green]✓[/bold green] url")
            else:
                if overwrite:
                    file_v["url"]["osf"] = osfstorage_data[file_v["fname"]]["guid"]
                    atlases_updated = True
                    console.print("    [bold yellow]↻[/bold yellow] url updated")
                else:
                    console.print(
                        f"    [bold red]x[/bold red] "
                        f"url local: {file_v['url']['osf']} "
                        f"remote: {osfstorage_data[file_v['fname']]['guid']}"
                    )

    console.print("\nANNOTS_META")
    for annot_meta in MOUSEMAPS_ANNOTS_META:
        console.print(f"{annot_meta['source']} {annot_meta['name']} >")
        console.print(r"  \[annot files] >")
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

        console.print(r"  \[aux files] >")
        for aux_k, aux_v in annot_meta["aux_files"].items():
            console.print(f"    {aux_k} >")

            if not isinstance(aux_v, list):
                aux_v = [aux_v]
            for file_v in aux_v:
                console.print(f"      {file_v['fname']} >")
                if file_v["fname"] not in osfstorage_data:
                    console.print(
                        f"        [bold red]x[/bold red] "
                        f"{file_v['fname']} not found in osfstorage"
                    )
                    continue
                if file_v["checksum"] == osfstorage_data[file_v["fname"]]["md5"]:
                    console.print("        [bold green]✓[/bold green] checksum")
                else:
                    if overwrite:
                        file_v["checksum"] = osfstorage_data[file_v["fname"]]["md5"]
                        annots_meta_updated = True
                        console.print(
                            "        [bold yellow]↻[/bold yellow] checksum updated"
                        )
                    else:
                        console.print(
                            f"        [bold red]x[/bold red] "
                            f"checksum local: {file_v['checksum']} "
                            f"remote: {osfstorage_data[file_v['fname']]['md5']}"
                        )
                if file_v["url"]["osf"] == osfstorage_data[file_v["fname"]]["guid"]:
                    console.print("        [bold green]✓[/bold green] url")
                else:
                    if overwrite:
                        file_v["url"]["osf"] = osfstorage_data[file_v["fname"]]["guid"]
                        annots_meta_updated = True
                        console.print(
                            "        [bold yellow]↻[/bold yellow] url updated"
                        )
                    else:
                        console.print(
                            f"        [bold red]x[/bold red] "
                            f"url local: {file_v['url']['osf']} "
                            f"remote: {osfstorage_data[file_v['fname']]['guid']}"
                        )

    console.print("\nANNOTS")
    for annot in MOUSEMAPS_ANNOTS:
        annotstr = "-".join(
            [annot["source"], annot["desc"], annot["space"], annot["res"]]
        )
        console.print(f"  {annotstr} >")
        if annot["fname"] not in osfstorage_data:
            console.print(
                f"        [bold red]x[/bold red] "
                f"{annot['fname']} not found in osfstorage"
            )
            continue
        if annot["checksum"] == osfstorage_data[annot["fname"]]["md5"]:
            console.print("    [bold green]✓[/bold green] checksum")
        else:
            if overwrite:
                annot["checksum"] = osfstorage_data[annot["fname"]]["md5"]
                annots_updated = True
                console.print("    [bold yellow]↻[/bold yellow] checksum updated")
            else:
                console.print(
                    f"    [bold red]x[/bold red] "
                    f"checksum local: {annot['checksum']} "
                    f"remote: {osfstorage_data[annot['fname']]['md5']}"
                )
        if annot["url"]["osf"] == osfstorage_data[annot["fname"]]["guid"]:
            console.print("    [bold green]✓[/bold green] url")
        else:
            if overwrite:
                annot["url"]["osf"] = osfstorage_data[annot["fname"]]["guid"]
                annots_updated = True
                console.print("    [bold yellow]↻[/bold yellow] url updated")
            else:
                console.print(
                    f"    [bold red]x[/bold red] "
                    f"url local: {annot['url']['osf']} "
                    f"remote: {osfstorage_data[annot['fname']]['guid']}"
                )

    # Write updated JSON files if changes were made
    if atlases_updated:
        atlases_data = {"atlases": MOUSEMAPS_ATLASES}
        if getattr(importlib.resources, "files", None) is not None:
            atlases_file = (
                importlib.resources.files("neuromaps_mouse")
                / "datasets/data/atlases.json"
            )
        else:
            from pkg_resources import resource_filename

            atlases_file = resource_filename(
                "neuromaps_mouse", "datasets/data/atlases.json"
            )
        with open(atlases_file, "w") as f:
            json.dump(atlases_data, f, indent=2)
        console.print("\n[bold green]✓[/bold green] Updated atlases.json")
    if annots_updated:
        annots_data = {"annotations": MOUSEMAPS_ANNOTS}
        if getattr(importlib.resources, "files", None) is not None:
            annots_file = (
                importlib.resources.files("neuromaps_mouse")
                / "datasets/data/annotations.json"
            )
        else:
            from pkg_resources import resource_filename

            annots_file = resource_filename(
                "neuromaps_mouse", "datasets/data/annotations.json"
            )
        with open(annots_file, "w") as f:
            json.dump(annots_data, f, indent=2)
        console.print("[bold green]✓[/bold green] Updated annotations.json")
    if annots_meta_updated:
        annots_meta_data = {"annotations-meta": MOUSEMAPS_ANNOTS_META}
        if getattr(importlib.resources, "files", None) is not None:
            annots_meta_file = (
                importlib.resources.files("neuromaps_mouse")
                / "datasets/data/annotations-meta.json"
            )
        else:
            from pkg_resources import resource_filename

            annots_meta_file = resource_filename(
                "neuromaps_mouse", "datasets/data/annotations-meta.json"
            )
        with open(annots_meta_file, "w") as f:
            json.dump(annots_meta_data, f, indent=2)
        console.print("[bold green]✓[/bold green] Updated annotations-meta.json")

    # Check for files in OSF storage that are not referenced in JSON files
    console.print("\nFILES IN OSF STORAGE NOT REFERENCED IN JSON")

    # Collect all filenames referenced in JSON files
    json_files = set()

    # Atlas files
    for atlas_v in MOUSEMAPS_ATLASES.values():
        for file_v in atlas_v["files"].values():
            json_files.add(file_v["fname"])

    # Annotation files
    for annot in MOUSEMAPS_ANNOTS:
        json_files.add(annot["fname"])

    # Annotation meta aux files
    for annot_meta in MOUSEMAPS_ANNOTS_META:
        for aux_v in annot_meta["aux_files"].values():
            if not isinstance(aux_v, list):
                aux_v = [aux_v]
            for file_v in aux_v:
                json_files.add(file_v["fname"])

    # Find files in OSF storage not in JSON
    unreferenced_files = set(osfstorage_data.keys()) - json_files

    if unreferenced_files:
        for fname in sorted(unreferenced_files):
            console.print(f"  [bold yellow]?[/bold yellow] {fname}")
        console.print(
            f"\n[bold yellow]Found {len(unreferenced_files)} "
            f"unreferenced files in OSF storage[/bold yellow]"
        )
    else:
        console.print(
            "  [bold green]✓[/bold green] All OSF storage files are referenced in JSON"
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
                            requests.get(
                                f"https://osf.io/{OSF_NODEID}/files/osfstorage{file['attributes']['path']}"
                            )
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
                        requests.get(
                            f"https://osf.io/{OSF_NODEID}/files/osfstorage{file['attributes']['path']}"
                        )
                    osfstorage_data[file["attributes"]["name"]] = {
                        "guid": file["attributes"]["guid"],
                        "md5": file["attributes"]["extra"]["hashes"]["md5"],
                    }
        else:
            raise ValueError(f"Unknown kind_path={kind_path}")
    return osfstorage_data


def _gen_doc_listofmaps_rst(listofmaps_file):
    """
    Generate a list of maps in reStructuredText format.

    For internal use only.
    """
    MOUSEMAPS_ANNOTS_META = _load_resource_json("datasets/data/annotations-meta.json")[
        "annotations-meta"
    ]

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
