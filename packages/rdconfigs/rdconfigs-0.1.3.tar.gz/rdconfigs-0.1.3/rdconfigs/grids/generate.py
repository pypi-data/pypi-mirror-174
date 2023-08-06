"""Ujan RoyBandyopadhyay
October 2022

This module provides tools for the generation of randomly colored
grids."""

import random

from rdconfigs.grids.type_aliases import RGB

def generate_grid(frequencies: dict[RGB, int],
                  rows: int, cols: int) -> list[list[RGB]]:
    """Return a grid (nested list) of RGB tuples.

    Arguments:
        - frequencies
            a dictionary whose keys are colors and values are the
            number of times each color should appear in the grid
        - rows
            the number of rows to generate
        - cols
            the number of squares to generate per row

    Raises:
        - ValueError if `sum(frequencies.values()) != rows*cols`

    Returns:
        - a list containing equal-sized lists of RGB values
    """
    grid_size = rows * cols
    if grid_size != sum(frequencies.values()):
        raise ValueError(f'cannot fill {rows}x{cols} grid '
                         f'with {sum(frequencies.values())} values')

    flat_grid = [None] * grid_size
    shuffled_squares = random.sample(range(grid_size), grid_size)
    start = 0

    for color in frequencies:
        assigned_squares = shuffled_squares[start : start+frequencies[color]]

        for square in assigned_squares:
            flat_grid[square] = color

        start += frequencies[color]

    return [flat_grid[row*cols : row*cols + cols] for row in range(rows)]
