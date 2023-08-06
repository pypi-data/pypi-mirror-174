"""Ujan RoyBandyopadhyay
October 2022

This module provides functions for analysis of randomly colored
grids."""

from rdconfigs.grids.type_aliases import RGB

def find_centroid(grid: list[list[RGB]], color: RGB) -> tuple[float, float]:
    """Return the position of a color's center of mass in a grid.

    Arguments:
        - grid
            a list containing equal-sized lists of RGB values
        - color
            the color whose center of mass to find

    Returns:
        - a (row, col) tuple containing the position of the color's
          center of mass on the grid
    """
    coordinates = get_graph(grid, color)

    row = sum(coordinate[0] for coordinate in coordinates) / len(coordinates)
    col = sum(coordinate[1] for coordinate in coordinates) / len(coordinates)

    return (row, col)

def find_centroids(grid: list[list[RGB]]) -> dict[RGB, tuple[float, float]]:
    """Return the centers of mass of each color in a grid.

    Arguments:
        - grid
            a list containing equal-sized lists of RGB values

    Returns:
        - a dictionary whose keys are colors and values are (row, col)
          tuples containing the position of the color's center of mass
          on the grid
    """
    colors = {square for row in grid for square in row}
    return {color: find_centroid(color) for color in colors}

def get_graph(grid: list[list[RGB]], /, *colors: RGB) -> set[tuple[int, int]]:
    """Return a set containing all squares of color.

    Positional arguments:
        - grid
            a list containing equal-sized lists of RGB values
        - *colors
            the color(s) to check for

    Returns:
        - a set containing (row, col) tuples representing each square
          of the given color
    """
    return {(i, j)
            for i, row in enumerate(grid)
            for j, square in enumerate(row)
            if square in colors}
