from .constants import *

def grid_to_abs_pos(val):
    x = int(val[0]) * (WIDTH + MARGIN) + (WIDTH / 2 + MARGIN)
    y = int(val[1]) * (HEIGHT + MARGIN) + (HEIGHT / 2 + MARGIN)
    return x, y

def abs_to_grid_pos(val):
    x = (val[0] - (WIDTH / 2 + MARGIN))// (WIDTH + MARGIN)
    y = (val[1] - (HEIGHT / 2 + MARGIN))// (HEIGHT + MARGIN)
    return x, y