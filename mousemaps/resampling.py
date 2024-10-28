import pandas as pd

from mousemaps.datasets import fetch_allenccfv3


def query_structure_graph_allenccfv3(
    data, in_col="acronym", out_col="all", data_dir=None, verbose=1
):
    # this directly returns the dataframe by indexing, so no none/null input
    df_struct = pd.read_csv(
        fetch_allenccfv3(
            which="structure-graph-csv", data_dir=data_dir, verbose=verbose
        )
    )
    if out_col == "all":
        return df_struct.set_index(in_col).loc[data, :].reset_index()
    else:
        return df_struct.set_index(in_col).loc[data, :].reset_index()[out_col]


def get_feature_allenccfv3(
    data, in_col="acronym", out_col="id", data_dir=None, verbose=1
):
    # this allows none/null input and returns a list
    df_struct = pd.read_csv(
        fetch_allenccfv3(
            which="structure-graph-csv", data_dir=data_dir, verbose=verbose
        )
    ).set_index(in_col)
    out_values = []
    for value in data:
        if pd.isna(value):  # or value is None:
            out_values.append(None)
        else:
            out_values.append(df_struct.loc[value, out_col])
    return out_values


def _get_nearest_ancestor_region_allenccfv3(
    source_region_ids, target_region_ids, include_self=True
):
    source_structure_id_paths = get_feature_allenccfv3(
        source_region_ids, in_col="id", out_col="structure_id_path", verbose=0
    )
    # print(source_structure_id_paths)
    matched_region_ids = []
    for p in source_structure_id_paths:
        if p is None:
            matched_region_ids.append(None)
            continue
        if include_self:
            p_list = list(map(int, p.split("/")[2:-1]))[
                ::-1
            ]  # reversed to get the nearest
        else:
            p_list = list(map(int, p.split("/")[2:-2]))[::-1]
        # print(p_list, target_region_ids)
        p_in_target = [_ in target_region_ids for _ in p_list]
        if any(p_in_target):
            _matched_id = p_list[p_in_target.index(True)]  # first match (nearest)
            matched_region_ids.append(_matched_id)
        else:
            # print(p)
            matched_region_ids.append(None)
    # print(matched_region_ids)
    return matched_region_ids


def _get_nearest_descendant_region_allenccfv3(
    source_region_ids, target_region_ids, include_self=True
):
    target_structure_id_paths = get_feature_allenccfv3(
        target_region_ids, in_col="id", out_col="structure_id_path", verbose=0
    )
    # print(source_structure_id_paths)
    matched_region_ids = []
    for p in source_region_ids:
        if p is None:
            matched_region_ids.append([])
            continue
        if include_self:
            tp_list = [
                list(map(int, tp.split("/")[2:-1])) for tp in target_structure_id_paths
            ]
        else:
            tp_list = [
                list(map(int, tp.split("/")[2:-2])) for tp in target_structure_id_paths
            ]
        p_in_tp = [_[-1] for _ in tp_list if p in _]

        matched_region_ids.append(p_in_tp)
    return matched_region_ids


def align_structures_allenccfv3(fixed, moving, ancester="fixed", debug=False):
    df_fixed = fixed.copy()
    df_moving = moving.copy()

    df_moving["id_ancestor_fixed"] = _get_nearest_ancestor_region_allenccfv3(
        df_moving["id"].tolist(), df_fixed["id"].tolist()
    )
    df_moving["id_ancestor_fixed"] = df_moving["id_ancestor_fixed"].astype("Int64")
    df_moving["id_descendant_fixed"] = _get_nearest_descendant_region_allenccfv3(
        df_moving["id"].tolist(), df_fixed["id"].tolist()
    )

    if debug:
        df_moving["id_ancestor_fixed_acronym"] = get_feature_allenccfv3(
            df_moving["id_ancestor_fixed"].tolist(),
            in_col="id",
            out_col="acronym",
            verbose=0,
        )
        df_moving["id_descendant_fixed_acronym"] = df_moving.apply(
            lambda x: get_feature_allenccfv3(
                x["id_descendant_fixed"], in_col="id", out_col="acronym", verbose=0
            )
            if len(["id_descendant_fixed"]) > 0
            else [],
            axis=1,
        )

    return df_fixed, df_moving


def match_allenccfv3_structures_fuzzy():
    pass
