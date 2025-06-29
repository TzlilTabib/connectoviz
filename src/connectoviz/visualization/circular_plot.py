import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import PathPatch
from matplotlib.path import Path


def plot_connectome_circle(matrix, region_names, ax=None):
    """
    Simple circular connectome plot with curved edges.

    Parameters
    ----------
    matrix : ndarray
        Square (N x N) matrix of connectivity values.
    region_names : list of str
        List of N region names in the same order as the matrix.
    ax : matplotlib axis, optional
        Axis to plot into (creates a new one if None).
    """
    # Input validation -----> do we need this here?
    if matrix.shape[0] != matrix.shape[1]:
        raise ValueError("Matrix must be square.")
    if matrix.shape[0] != len(region_names):
        raise ValueError("Region names must match matrix size.")

    # Calculate coordinates for nodes in a circular layout
    n_nodes = len(region_names)
    angles = np.linspace(0, 2 * np.pi, n_nodes, endpoint=False)
    coords = np.c_[np.cos(angles), np.sin(angles)]

    # Set up the figure and axis (if not provided)
    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 8))
        ax.axis('off')

    # Draw nodes
    for i, (x, y) in enumerate(coords):
        ax.plot(x, y, 'o', color='black')
        ax.text(x * 1.1, y * 1.1, region_names[i], ha='center', va='center')

    # Draw edges (connections)
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

    # Show the plot
    if ax is None:
        plt.show()
