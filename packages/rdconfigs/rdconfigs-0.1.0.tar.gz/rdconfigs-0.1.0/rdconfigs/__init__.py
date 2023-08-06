"""Ujan RoyBandyopadhyay
October 2022

Generate, display, and analyze randomly colored grids.

Example usage:
>>> frequencies = {(0, 0, 0): 3, (255, 255, 255): 6}
>>> g = generate_grid(frequencies, rows=3, cols=3)
>>> print(g)
[[(0, 0, 0), (255, 255, 255), (255, 255, 255)],
 [(255, 255, 255), (0, 0, 0), (255, 255, 255)],
 [(255, 255, 255), (255, 255, 255), (0, 0, 0)]]
>>> display(g)  # display `g` in a new window
"""

__all__ = ['display', 'find_centroid', 'find_centroids', 'generate_grid',
           'get_graph', 'RGB']

from random_tiling.grids.analysis import (
    find_centroid, find_centroids, get_graph
)
from random_tiling.grids.generate import generate_grid
from random_tiling.grids.type_aliases import RGB
from random_tiling.ui.ui_tools import display
