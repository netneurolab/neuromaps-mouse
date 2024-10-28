import tempfile
from pathlib import Path

import h5py
import matplotlib.image
import matplotlib.pyplot as plt
import numpy as np
import trimesh
from matplotlib import colors as mcolors
from matplotlib.cm import ScalarMappable
from matplotlib.collections import LineCollection, PolyCollection
from matplotlib.colors import Normalize
from mpl_toolkits.axes_grid1.anchored_artists import AnchoredSizeBar
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

from mousemaps.datasets import fetch_allenccfv3
from mousemaps.resampling import query_structure_graph_allenccfv3

VIEW_TO_BASIS = {
    "coronal": np.array([1, 0, 0]),
    "axial": np.array([0, 1, 0]),
    "sagittal": np.array([0, 0, 1])
}


def _extend_halfwidth(a, b, hw):
    c = (a + b) / 2
    return c - hw, c + hw


def _get_allenccfv3_constants():
    with h5py.File(fetch_allenccfv3(which="structure-mesh", verbose=0), "r") as f:
        root_mesh = trimesh.Trimesh(
            vertices=f["997/vertices"][:], faces=f["997/faces"][:])
    return {
        "center_mass": root_mesh.center_mass,
        "bounds": root_mesh.bounds,
        "max_hw": np.max(np.diff(root_mesh.bounds, axis=0)) / 2
    }


def _filter_allenccfv3_available_regions(regions, values, verbose=1):

    region_ids = query_structure_graph_allenccfv3(
        regions, in_col="acronym", out_col="id", verbose=0)["id"].tolist()

    with h5py.File(fetch_allenccfv3(which="structure-mesh", verbose=0), "r") as f:
        mesh_keys = list(map(int, f.keys()))

    avail_indices = [i for i, v in enumerate(region_ids) if v in mesh_keys]
    region_ids_avail = np.array(region_ids)[avail_indices]
    regions_avail = np.array(regions)[avail_indices]
    values_avail = np.array(values)[avail_indices]

    if len(regions_avail) < len(regions) and verbose:
        print(
            "Warning: these regions are not found in the structure meshes, "
            "so they are not plotted: "
            f"{[_ for _ in regions if _ not in regions_avail]}"
        )
    return region_ids_avail, regions_avail, values_avail


def plot_allenccfv3_ortho(
    regions, values, 
    section_coords=(6587.84, 3849.08, 5688.16),
    cmap="viridis",
    clim=None,
    cnorm=None,
    show_colorbar=True,
    cbar_title=None,
    equal_scale=True,
    equal_scale_zoom=1,
    show_scale=True,
    show_coord=True,
    figsize=(3, 1),
    cbar_kws=None,
    lc_kws=None,
    pc_kws=None,
    verbose=1
):

    if cnorm is None:
        if clim is not None:
            _vmin, _vmax = clim
        else:
            _vmin, _vmax = np.nanpercentile(values, [2.5, 97.5])
        cnorm = mcolors.Normalize(vmin=_vmin, vmax=_vmax, clip=False)

    lc_dict = {"color": "0.3", "lw": 0.5}

    lc_dict.update(lc_kws or {})
    pc_dict = pc_kws or {}
    cbar_dict = cbar_kws or {}

    region_ids_avail, regions_avail, values_avail = _filter_allenccfv3_available_regions(regions, values, verbose=verbose)
    
    bg_const = _get_allenccfv3_constants()
    
    with h5py.File(fetch_allenccfv3(which="structure-mesh", verbose=0), "r") as f:
        root_mesh = trimesh.Trimesh(vertices=f["997/vertices"][:], faces=f["997/faces"][:])
        mesh_list = [
            trimesh.Trimesh(vertices=f[f"{_}/vertices"][:], faces=f[f"{_}/faces"][:]) for _ in region_ids_avail]
    
    fig, axes = plt.subplots(1, 3, figsize=figsize, width_ratios=[1, 1, 1], gridspec_kw={"wspace": 0})

    for i_ax, (ax, view) in enumerate(zip(axes.flatten(), VIEW_TO_BASIS.keys())):
        # get sections
        view_index = list(VIEW_TO_BASIS.keys()).index(view)
        curr_bg_segs = root_mesh.section_multiplane(
            plane_origin=VIEW_TO_BASIS[view] * section_coords[view_index], 
            plane_normal=VIEW_TO_BASIS[view], 
            heights=[0]
        )[0]
        if curr_bg_segs is not None:
            curr_bg_segs = curr_bg_segs.discrete

        sections = [
            m.section_multiplane(
                plane_origin=VIEW_TO_BASIS[view]*section_coords[i_ax], 
                plane_normal=VIEW_TO_BASIS[view], heights=[0]
            )[0] for m in mesh_list
        ]
        # get segments
        segs, seg_colors = [], []
        for i_sec, sec in enumerate(sections):
            if sec is not None:
                curr_seg = sec.discrete
                segs += curr_seg
                seg_colors += [values_avail[i_sec]] * len(curr_seg)
        # plot background
        ax.add_collection(LineCollection(segments=curr_bg_segs, color="darkgray", lw=1))
        ax.add_collection(PolyCollection(verts=curr_bg_segs, color="gainsboro"))
        # plot data
        ax.add_collection(LineCollection(segments=segs, **lc_dict))
        pc = PolyCollection(verts=segs, norm=cnorm, cmap=cmap, **pc_dict)
        pc.set_array(seg_colors)
        ax.add_collection(pc)
        #
        if show_scale:
            ax.add_artist(
                AnchoredSizeBar(ax.transData, 2000, "2000", loc="lower left", frameon=False)
            )
        #
        if show_coord:
            ax.text(0.5, 0.95, f"{chr(i_ax+88)} = {section_coords[i_ax]}", ha="center", transform=ax.transAxes)
        #
        ax.set_aspect("equal", adjustable="datalim")
        ax.set_box_aspect(1)
        if view != "axial":
            ax.invert_yaxis()
        ax.axis("off")

        if equal_scale:
            ax.autoscale_view() # re-calculate the limits
            ax.set_xlim(_extend_halfwidth(*ax.get_xlim(), bg_const["max_hw"]*1/equal_scale_zoom))
            ax.set_ylim(_extend_halfwidth(*ax.get_ylim(), bg_const["max_hw"]*1/equal_scale_zoom))
        else:
            ax.autoscale()
    
    if show_colorbar:
        cax = inset_axes(axes[-1], width=1, height=0.1, loc="lower right")
        cbar = fig.colorbar(ScalarMappable(cmap=cmap, norm=cnorm), cax=cax, orientation="horizontal")
        if cbar_title is not None:
            cbar.ax.set_xlabel(cbar_title)
            cbar.ax.xaxis.set_label_position('top') 
            
        cbar.ax.set(**cbar_dict)
    return fig, axes


def plot_allenccfv3_ortho_asym(
    regions_lh, regions_rh, values_lh, values_rh,
    section_coords=(6587.84, 3849.08, 5688.16),
    cmap="viridis",
    clim=None,
    cnorm=None,
    show_colorbar=True,
    cbar_title=None,
    equal_scale=True,
    equal_scale_zoom=1,
    show_scale=True,
    show_coord=True,
    figsize=(3, 1),
    cbar_kws=None,
    lc_kws=None,
    pc_kws=None,
    verbose=1
):
    if cnorm is None:
        if clim is not None:
            _vmin, _vmax = clim
        else:
            _vmin, _vmax = np.nanpercentile(np.r_[values_lh, values_rh], [2.5, 97.5])
        cnorm = mcolors.Normalize(vmin=_vmin, vmax=_vmax, clip=False)


    def _plot_one_hemi(regions, values):
        return plot_allenccfv3_ortho(
            regions, values, 
            section_coords=section_coords,
            cmap=cmap,
            # clim=clim,
            cnorm=cnorm,
            show_colorbar=show_colorbar,
            cbar_title=cbar_title,
            equal_scale=equal_scale,
            equal_scale_zoom=equal_scale_zoom,
            show_scale=show_scale,
            show_coord=show_coord,
            figsize=figsize,
            cbar_kws=cbar_kws,
            lc_kws=lc_kws,
            pc_kws=pc_kws,
            verbose=verbose
        )

    fig_lh, axes_lh = _plot_one_hemi(regions_lh, values_lh)
    fig_rh, axes_rh = _plot_one_hemi(regions_rh, values_rh)

    fig_lh.canvas.draw()
    fig_rh.canvas.draw()
    
    fig_lh_im = np.frombuffer(fig_lh.canvas.buffer_rgba(), dtype=np.uint8).reshape(fig_lh.canvas.get_width_height()[::-1] + (4,))
    fig_rh_im = np.frombuffer(fig_rh.canvas.buffer_rgba(), dtype=np.uint8).reshape(fig_rh.canvas.get_width_height()[::-1] + (4,))

    plt.close(fig_lh)
    plt.close(fig_rh)
    
    h_px, w_px, _ = fig_lh_im.shape
    
    positions = [ax.get_position(original=False) for ax in axes_lh]
    coords = [(int(w_px * pos.xmin), int(w_px * (pos.xmin + pos.xmax) / 2), int(w_px * pos.xmax)) for pos in positions]
    
    z_center = 5688.16
    # (300, 900)
    # coords = [(113, 228, 344), (345, 461, 576), (578, 693, 809)]
    new_im = np.concatenate(
        [
            fig_lh_im[:, 0:coords[0][1], :], # (0, 228)
            fig_rh_im[:, coords[0][1]:coords[0][2], :], # (228, 344)
            fig_lh_im[:, coords[0][2]:coords[1][1], :], # (344, 461)
            fig_rh_im[:, coords[1][1]:coords[1][2], :], # (461, 576)
            fig_lh_im[:, coords[1][2]:coords[2][1], :] if section_coords[-1] <= z_center else fig_rh_im[:, coords[1][2]:coords[2][1], :], # (576, 693)
            fig_lh_im[:, coords[2][1]:w_px, :] if section_coords[-1] <= z_center else fig_rh_im[:, coords[2][1]:w_px, :] # (693, 900)
        ],
        axis=1
    )
    fig, ax = plt.subplots(figsize=figsize, gridspec_kw={"left": 0, "right": 1, "bottom": 0, "top": 1})
    ax.imshow(new_im)
    ax.axis("off")

    return fig, ax


def plot_allenccfv3_lightbox(
    regions, values,
    view="coronal",
    slices=[1000, 2000, 3000],
    cmap="viridis",
    clim=None,
    cnorm=None,
    show_colorbar=True,
    cbar_title=None,
    equal_scale=True,
    equal_scale_zoom=1,
    show_scale=True,
    show_coord=True,
    figsize=None,
    cbar_kws=None,
    lc_kws=None,
    pc_kws=None,
    verbose=1
):
    if not isinstance(slices, list):
        slices = [slices]
    if figsize is None:
        figsize=(len(slices), 1)

    if cnorm is None:
        if clim is not None:
            _vmin, _vmax = clim
        else:
            _vmin, _vmax = np.nanpercentile(values, [2.5, 97.5])
        cnorm = mcolors.Normalize(vmin=_vmin, vmax=_vmax, clip=False)

    lc_dict = {"color": "0.3", "lw": 0.5}
    pc_dict = {}
    cbar_dict = {}

    if lc_kws is not None:
        lc_dict.update(lc_kws)
    if pc_kws is not None:
        pc_dict.update(pc_kws)
    if cbar_kws is not None:
        cbar_dict.update(cbar_kws)

    region_ids_avail, regions_avail, values_avail = _filter_allenccfv3_available_regions(regions, values, verbose=verbose)

    with h5py.File(fetch_allenccfv3(which="structure-mesh", verbose=0), "r") as f:
        root_mesh = trimesh.Trimesh(vertices=f["997/vertices"][:], faces=f["997/faces"][:])
        mesh_list = [
            trimesh.Trimesh(vertices=f[f"{_}/vertices"][:], faces=f[f"{_}/faces"][:]) for _ in region_ids_avail]


    bg_segs_list = root_mesh.section_multiplane(
            plane_origin=[0, 0, 0], 
            plane_normal=VIEW_TO_BASIS[view], 
            heights=slices
        )
    slices_segs_list = [
            m.section_multiplane(
                plane_origin=[0, 0, 0], 
                plane_normal=VIEW_TO_BASIS[view], heights=slices
            ) for m in mesh_list
        ]
    bg_const = _get_allenccfv3_constants()
    view_index = list(VIEW_TO_BASIS.keys()).index(view)
    
    fig, axes = plt.subplots(
        1, len(slices), figsize=figsize, width_ratios=[1]*len(slices), gridspec_kw={"wspace": 0})

    for i_ax, (ax, coord) in enumerate(zip(axes.flatten(), slices)):
        curr_bg_segs = bg_segs_list[i_ax]
        if curr_bg_segs is not None:
             curr_bg_segs = curr_bg_segs.discrete
        sections = [_[i_ax] for _ in slices_segs_list]

        # get segments
        segs, seg_colors = [], []
        for i_sec, sec in enumerate(sections):
            if sec is not None:
                curr_seg = sec.discrete
                segs += curr_seg
                seg_colors += [values_avail[i_sec]] * len(curr_seg)
        
        # plot background
        ax.add_collection(LineCollection(segments=curr_bg_segs, color="darkgray", lw=1))
        ax.add_collection(PolyCollection(verts=curr_bg_segs, color="gainsboro"))
        # plot data
        ax.add_collection(LineCollection(segments=segs, **lc_dict))
        pc = PolyCollection(verts=segs, norm=cnorm, cmap=cmap, **pc_dict)
        pc.set_array(seg_colors)
        ax.add_collection(pc)
        #
        if show_scale:
            ax.add_artist(
                AnchoredSizeBar(ax.transData, 2000, "2000", loc="lower left", frameon=False)
            )
        #
        if show_coord:
            ax.text(0.5, 0.95, f"{chr(view_index+88)} = {slices[i_ax]}", ha="center", transform=ax.transAxes)
        #
        ax.set_aspect("equal", adjustable="datalim")
        ax.set_box_aspect(1)
        if view != "axial":
            ax.invert_yaxis()
        ax.axis("off")

        if equal_scale:
            ax.autoscale_view() # re-calculate the limits
            ax.set_xlim(_extend_halfwidth(*ax.get_xlim(), bg_const["max_hw"]*1/equal_scale_zoom))
            ax.set_ylim(_extend_halfwidth(*ax.get_ylim(), bg_const["max_hw"]*1/equal_scale_zoom))
        else:
            ax.autoscale()

    if show_colorbar:
        cax = inset_axes(axes[-1], width=1, height=0.1, loc="lower right")
        cbar = fig.colorbar(ScalarMappable(cmap=cmap, norm=cnorm), cax=cax, orientation="horizontal")
        if cbar_title is not None:
            cbar.ax.set_xlabel(cbar_title)
            cbar.ax.xaxis.set_label_position('top') 
            
        cbar.ax.set(**cbar_dict)

    return fig, axes

def plot_allenccfv3_3d():
    pass