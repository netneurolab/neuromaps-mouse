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
        match = True
        for key in ["source", "desc", "space", "res", "format"]:
            value = keys_dict[key]
            if value is not None and annot[key] != value:
                match = False
                break
        if keys_dict["tag"] is not None and keys_dict["tag"] not in annot["tags"]:
            match = False
        if match:
            filtered.append(annot)
    return filtered


def _check_osfstorage():
    """
    Check for errors in OSF links.

    For internal use only.

    osfstorage_data = _check_osfstorage()

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

    def _get_file_href(entry):
        return entry["relationships"]["files"]["links"]["related"]["href"]

    def _get_paginated(url):
        resp = requests.get(url).json()
        results = resp["data"]
        while resp["links"].get("next"):
            resp = requests.get(resp["links"]["next"]).json()
            results.extend(resp["data"])
        return results

    def _process_file(file_entry):
        attrs = file_entry["attributes"]
        console.print(f"      {attrs['guid']}")
        console.print(f"      {attrs['extra']['hashes']['md5']}")
        if not attrs["guid"]:
            r = requests.get(
                file_entry["links"]["self"] + "?create_guid=true",
                allow_redirects=True,
            )
            console.print(f"      {r.url}")
        osfstorage_data[attrs["name"]] = {
            "guid": attrs["guid"],
            "md5": attrs["extra"]["hashes"]["md5"],
        }

    for kind in requests.get(OSF_URL).json()["data"]:
        kind_path = kind["attributes"]["materialized_path"]
        console.print(f"{kind_path} >")
        if kind_path == "/atlases/":
            for source in _get_paginated(_get_file_href(kind)):
                source_path = source["attributes"]["materialized_path"]
                console.print(f"  {source_path.removeprefix(kind_path)} >")
                for version in _get_paginated(_get_file_href(source)):
                    version_path = version["attributes"]["materialized_path"]
                    console.print(f"  {version_path.removeprefix(source_path)} >")
                    for file_entry in _get_paginated(_get_file_href(version)):
                        fpath = file_entry["attributes"]["materialized_path"]
                        console.print(f"    {fpath.removeprefix(version_path)} >")
                        _process_file(file_entry)
        elif kind_path == "/annotations/":
            for source in _get_paginated(_get_file_href(kind)):
                source_path = source["attributes"]["materialized_path"]
                console.print(f"  {source_path.removeprefix(kind_path)} >")
                for file_entry in _get_paginated(_get_file_href(source)):
                    fpath = file_entry["attributes"]["materialized_path"]
                    console.print(f"    {fpath.removeprefix(source_path)} >")
                    _process_file(file_entry)
        else:
            raise ValueError(f"Unknown kind_path={kind_path}")
    return osfstorage_data


def _write_resource_json(relative_path, data):
    """Write data dict to a package resource JSON file."""
    if getattr(importlib.resources, "files", None) is not None:
        filepath = importlib.resources.files("neuromaps_mouse") / relative_path
    else:
        from pkg_resources import resource_filename

        filepath = resource_filename("neuromaps_mouse", relative_path)
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)


def _validate_file_fields(file_entry, osfstorage_data, overwrite, console, indent="    "):
    """Validate checksum and URL of a file entry against OSF storage data.

    Returns True if any field was updated, None if file not in osfstorage_data.
    """
    fname = file_entry["fname"]
    if fname not in osfstorage_data:
        console.print(f"{indent}[bold red]x[/bold red] {fname} not found in osfstorage")
        return None

    updated = False
    remote = osfstorage_data[fname]

    if file_entry["checksum"] == remote["md5"]:
        console.print(f"{indent}[bold green]✓[/bold green] checksum")
    elif overwrite:
        file_entry["checksum"] = remote["md5"]
        updated = True
        console.print(f"{indent}[bold yellow]↻[/bold yellow] checksum updated")
    else:
        console.print(
            f"{indent}[bold red]x[/bold red] "
            f"checksum local: {file_entry['checksum']} remote: {remote['md5']}"
        )

    if file_entry["url"]["osf"] == remote["guid"]:
        console.print(f"{indent}[bold green]✓[/bold green] url")
    elif overwrite:
        file_entry["url"]["osf"] = remote["guid"]
        updated = True
        console.print(f"{indent}[bold yellow]↻[/bold yellow] url updated")
    else:
        console.print(
            f"{indent}[bold red]x[/bold red] "
            f"url local: {file_entry['url']['osf']} remote: {remote['guid']}"
        )

    return updated


def _check_json(osfstorage_data, overwrite=False):
    """
    Check for errors in meta.json.

    For internal use only.

    _check_json(osfstorage_data)

    Returns
    -------
    None
    """
    from rich.console import Console

    console = Console()

    MOUSEMAPS_ATLASES = _load_resource_json("datasets/data/atlases.json")["atlases"]
    MOUSEMAPS_ANNOTS = _load_resource_json("datasets/data/annotations.json")[
        "annotations"
    ]
    MOUSEMAPS_ANNOTS_META = _load_resource_json("datasets/data/annotations-meta.json")[
        "annotations-meta"
    ]

    atlases_updated = False
    annots_updated = False
    annots_meta_updated = False

    console.print("ATLASES")
    for atlas_k, atlas_v in MOUSEMAPS_ATLASES.items():
        console.print(f"{atlas_k} >")
        for file_k, file_v in atlas_v["files"].items():
            console.print(f"  {file_k} >")
            if _validate_file_fields(file_v, osfstorage_data, overwrite, console, "    "):
                atlases_updated = True

    console.print("\nANNOTS_META")
    for annot_meta in MOUSEMAPS_ANNOTS_META:
        console.print(f"{annot_meta['source']} {annot_meta['name']} >")
        console.print(r"  \[annot files] >")
        for file_v in annot_meta["files"]:
            console.print(f"    {'-'.join(file_v)} >")
            try:
                matched = _match_annots_by_tuple([tuple(file_v)])
            except ValueError:
                console.print("      [bold red]x[/bold red] json not found")
            else:
                if len(matched) == 1:
                    console.print("      [bold green]✓[/bold green] json")
                else:
                    console.print(f"      [bold red]x[/bold red] json {len(matched) = }")

        console.print(r"  \[aux files] >")
        for aux_k, aux_v in annot_meta["aux_files"].items():
            console.print(f"    {aux_k} >")
            if not isinstance(aux_v, list):
                aux_v = [aux_v]
            for file_v in aux_v:
                console.print(f"      {file_v['fname']} >")
                if _validate_file_fields(
                    file_v, osfstorage_data, overwrite, console, "        "
                ):
                    annots_meta_updated = True

    console.print("\nANNOTS")
    for annot in MOUSEMAPS_ANNOTS:
        annotstr = "-".join(
            [annot["source"], annot["desc"], annot["space"], annot["res"]]
        )
        console.print(f"  {annotstr} >")
        if _validate_file_fields(annot, osfstorage_data, overwrite, console, "    "):
            annots_updated = True

    if atlases_updated:
        _write_resource_json("datasets/data/atlases.json", {"atlases": MOUSEMAPS_ATLASES})
        console.print("\n[bold green]✓[/bold green] Updated atlases.json")
    if annots_updated:
        _write_resource_json(
            "datasets/data/annotations.json", {"annotations": MOUSEMAPS_ANNOTS}
        )
        console.print("[bold green]✓[/bold green] Updated annotations.json")
    if annots_meta_updated:
        _write_resource_json(
            "datasets/data/annotations-meta.json",
            {"annotations-meta": MOUSEMAPS_ANNOTS_META},
        )
        console.print("[bold green]✓[/bold green] Updated annotations-meta.json")

    # Check for unreferenced files
    console.print("\nFILES IN OSF STORAGE NOT REFERENCED IN JSON")
    json_files = set()
    for atlas_v in MOUSEMAPS_ATLASES.values():
        for file_v in atlas_v["files"].values():
            json_files.add(file_v["fname"])
    for annot in MOUSEMAPS_ANNOTS:
        json_files.add(annot["fname"])
    for annot_meta in MOUSEMAPS_ANNOTS_META:
        for aux_v in annot_meta["aux_files"].values():
            if not isinstance(aux_v, list):
                aux_v = [aux_v]
            for file_v in aux_v:
                json_files.add(file_v["fname"])

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





def _gen_doc_listofmaps_rst(listofmaps_file):
    """
    Generate a list of maps in reStructuredText format.

    For internal use only.
    """
    MOUSEMAPS_ANNOTS_META = _load_resource_json("datasets/data/annotations-meta.json")[
        "annotations-meta"
    ]

    sections = []

    for annot_meta in MOUSEMAPS_ANNOTS_META:
        lines = []
        title = f"{annot_meta['name']} ({annot_meta['source']})"
        lines += [
            title,
            "=" * len(title),
            "",
            annot_meta["description"],
            "",
        ]

        if annot_meta.get("warning"):
            lines += [
                f".. warning:: {annot_meta['warning']}",
                "",
            ]

        # File list as a table: description, format, fetch key
        lines += [
            "**Available files**",
            "",
            ".. list-table::",
            "   :header-rows: 1",
            "",
            "   * - Description",
            "     - Format",
            "     - Key",
        ]
        for file_tuple in annot_meta["files"]:
            curr_annot = _match_annots_by_tuple(tuple(file_tuple))[0]
            desc = annot_meta["file_desc"][curr_annot["desc"]]
            fmt = curr_annot["format"]
            key_str = ", ".join(
                f"'{curr_annot[k]}'" for k in ("source", "desc", "space", "res")
            )
            lines += [
                f"   * - {desc}",
                f"     - {fmt}",
                f"     - ``({key_str})``",
            ]
        lines.append("")

        # Unified how-to-use section
        first_annot = _match_annots_by_tuple(tuple(annot_meta["files"][0]))[0]
        first_key = ", ".join(
            f"'{first_annot[k]}'" for k in ("source", "desc", "space", "res")
        )
        lines += [
            "**How to use**",
            "",
            ".. code:: python",
            "",
            "    # fetch a specific annotation",
            f"    fetch_annotation(({first_key}))",
            "",
            "    # file location",
            f"    # $MOUSEMAPS_DATA/{first_annot['rel_path']}",
            "",
        ]

        # List all region mapping files from aux_files
        aux = annot_meta.get("aux_files", {})
        regionmaps = aux.get("regionmapping", [])
        if not isinstance(regionmaps, list):
            regionmaps = [regionmaps]
        if regionmaps:
            lines.append("    # region mapping files")
            for rm in regionmaps:
                lines.append(f"    # {rm['fname']}")
            lines.append("")

        # List all feature mapping files from aux_files
        featmaps = aux.get("featuremapping", [])
        if not isinstance(featmaps, list):
            featmaps = [featmaps]
        if featmaps:
            lines.append("    # feature mapping files")
            for fm in featmaps:
                lines.append(f"    # {fm['fname']}")
            lines.append("")

        valid_refs = [
            ref for ref in annot_meta["refs"]
            if ref.get("bibkey") not in ("", None)
        ]
        if valid_refs:
            lines += [
                "**References**",
                "",
            ]
            for ref in valid_refs:
                lines.append(f"    - {ref['citation']}")

        sections.append("\n".join(lines))

    header = "\n".join([
        ".. _listofmaps:",
        "",
        "------------",
        "List of Maps",
        "------------",
        "This is a complete list of maps available in the `neuromaps_mouse` package.",
    ])

    separator = "\n\n----\n\n"

    with open(listofmaps_file, "w") as dst:
        dst.write(header + separator + separator.join(sections) + "\n")
