import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import PathPatch
from matplotlib.path import Path
import matplotlib.cm as cm
import matplotlib.colors as mcolors


def plot_connectome_circle(
        matrix,
        region_names,
        group_labels=None,
        group_colors=None,
        group_cmap="tab20b",
        ax=None):
    """
    Simple circular connectome plot with curved edges.

    Parameters
    ----------
    matrix : ndarray
        Square (N x N) matrix of connectivity values.
    region_names : list of str
        List of N region names in the same order as the matrix.
    group_labels : list of str or int, optional
        Group label for each region, used for node coloring.
    group_colors : dict, optional
        Mapping of group labels to colors. Overrides colormap.
    group_cmap : str, default="tab20b"
        Name of matplotlib colormap to use if group_colors is not provided.
    ax : matplotlib axis, optional
        Axis to plot into (creates a new one if None).
    """
    # ---------- Input validation ----------
    if matrix.shape[0] != matrix.shape[1]:
        raise ValueError("Matrix must be square.")
    if matrix.shape[0] != len(region_names):
        raise ValueError("Region names must match matrix size.")

    # ---------- Calculate circular layout ----------
    n_nodes = len(region_names)
    angles = np.linspace(0, 2 * np.pi, n_nodes, endpoint=False)
    coords = np.c_[np.cos(angles), np.sin(angles)]

    # ---------- Determine node colors ----------
    node_colors = _assign_node_colors(
        group_labels, group_colors, group_cmap, n_nodes)

    # ---------- Set up the figure and axis (if not provided) ----------
    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 8))
        ax.axis('off')

    # ---------- Draw nodes ----------
    _draw_nodes(ax, coords, node_colors, region_names)

    # ---------- Draw edges (connections) ----------
    _draw_edges(ax, coords, matrix)

    # ---------- Show the plot ----------
    if ax is None:
        plt.show()

# === Helper functions ===
def _assign_node_colors(group_labels, group_colors, group_cmap, n_nodes):
    """
    Assign colors to nodes based on group labels or a colormap.

    Parameters
    ----------
    group_labels : list of str or int, optional
        Group label for each node.
    group_colors : dict, optional
        Mapping of group labels to specific colors.
    group_cmap : str
        Name of the colormap to use if no group_colors are provided.
    n_nodes : int
        Number of nodes.

    Returns
    -------
    list
        List of colors for each node.
    """
    if group_labels is None:
        return ["black"] * n_nodes

    if len(group_labels) != n_nodes:
        raise ValueError("Length of group_labels must match number of nodes.")

    unique_groups = sorted(set(group_labels))

    if group_colors is not None:
        # Ensure all groups have a color
        missing = [g for g in unique_groups if g not in group_colors]
        if missing:
            raise ValueError(f"Missing colors for groups: {missing}")
        return [group_colors[label] for label in group_labels]

    # Else: assign one color per unique group using a colormap
    cmap = cm.get_cmap(group_cmap, len(unique_groups))
    color_map = {group: cmap(i) for i, group in enumerate(unique_groups)}
    return [color_map[label] for label in group_labels]

def _draw_nodes(ax, coords, node_colors, region_names):
    """
    Draw nodes on the axis.

    Parameters
    ----------
    ax : matplotlib axis
        Axis to draw on.
    coords : ndarray
        Coordinates of the nodes.
    node_colors : list
        Colors for each node.
    region_names : list of str
        Names of the regions.
    """
    for i, (x, y) in enumerate(coords):
        ax.plot(x, y, 'o', color=node_colors[i])
        ax.text(x * 1.1, y * 1.1, region_names[i], ha='center', va='center')

def _draw_edges(ax, coords, matrix):
    """
    Draw edges (connections) between nodes.

    Parameters
    ----------
    ax : matplotlib axis
        Axis to draw on.
    coords : ndarray
        Coordinates of the nodes.
    matrix : ndarray
        Connectivity matrix.
    """
    n_nodes = len(coords)
    for i in range(n_nodes):
        for j in range(i + 1, n_nodes):
            weight = matrix[i, j]
            if weight > 0:
                x1, y1 = coords[i]
                x2, y2 = coords[j]

                verts = [(x1, y1), (0, 0), (x2, y2)]
                codes = [Path.MOVETO, Path.CURVE3, Path.CURVE3]
                path = Path(verts, codes)
                patch = PathPatch(path, edgecolor='blue', lw=weight * 5, alpha=0.5, facecolor='none')
                ax.add_patch(patch)