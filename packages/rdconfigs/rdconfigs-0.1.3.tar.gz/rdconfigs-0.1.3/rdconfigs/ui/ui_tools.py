"""Ujan RoyBandyopadhyay
October 2022

This module provides functions for displaying grids using pygame."""

import pygame as pg

from rdconfigs.grids.type_aliases import RGB

def display(grid: list[list[RGB]], *,
            square_width: int = 5, square_height: int = 5,
            border: int = 0, title: str = 'Tiles',
            border_color: RGB = (0, 0, 0)):
    """Display a grid of colors in a new window.

    Arguments:
        - grid
            a list containing equal-sized lists of RGB values

    Keyword Arguments:
        - square_width
            the width (in pixels) of each displayed square
        - square_height
            the height (in pixels) of each displayed square
        - border
            the width (in pixels) of the border drawn between squares
        - title
            the title of the display window
        - border_color
            the color of the border between squares
    """
    rows, cols = len(grid), len(grid[0])
    height, width = rows * square_height, cols * square_width

    pg.init()

    window = pg.display.set_mode((width, height))
    pg.display.set_caption(title)
    window.fill(border_color)
    fill_grid(grid, window, border=border)
    pg.display.update()

    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
                break

    pg.quit()

def fill_grid(grid: list[list[RGB]], window: pg.Surface, *, border: int = 0):
    """Draw grid on window.

    Arguments:
        - grid
            a list containing equal-sized lists of RGB values
        - window
            pygame surface to draw grid onto

    Keyword Arguments:
        - border
            width (in pixels) of border to draw between squares
    """
    square_width = window.get_width() // len(grid)
    square_height = window.get_height() // len(grid[0])

    for i, row in enumerate(grid):
        for j, color in enumerate(row):
            fill_square((i, j), color, window,
                        square_width=square_width,
                        square_height=square_height,
                        border=border)

def fill_square(square: tuple[int, int], color: RGB, window: pg.Surface, *,
                square_width: int, square_height: int, border: int = 0):
    """Fill square in window with color.

    Arguments:
        - square
            coordinate of square (row, col)
        - color
            color with which to fill square
        - window
            pygame surface where square is located

    Keyword Arguments:
        - square_width
            pixel width of each square in window
        - square_height
            pixel height of each square in window
        - border
            pixel width of border between squares
    """
    row, col = square
    rect = pg.Rect(col*square_width + border,
                   row*square_height + border,
                   square_width - border,
                   square_height - border)
    window.fill(color, rect)
