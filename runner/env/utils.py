from .constants import *
import numpy as np

def grid_to_abs_pos(val):
    x = int(val[0]) * (WIDTH + MARGIN) + (WIDTH / 2 + MARGIN)
    y = int(val[1]) * (HEIGHT + MARGIN) + (HEIGHT / 2 + MARGIN)
    return x, y

def abs_to_grid_pos(val):
    x = (val[0] - (WIDTH / 2 + MARGIN))// (WIDTH + MARGIN)
    y = (val[1] - (HEIGHT / 2 + MARGIN))// (HEIGHT + MARGIN)
    return x, y


def to_json(obj):
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, list) or isinstance(obj, tuple):
        return [to_json(s) for s in obj]
    elif isinstance(obj, dict):
        out = {}
        for k in obj:
            out[k] = to_json(obj[k])
        return out
    else:
        return obj