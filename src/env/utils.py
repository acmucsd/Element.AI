from .grid import game as Grid
from .angular import game as Angular
from .grid import constants as GRID_CONSTANTS
from .angular import constants as ANGULAR_CONSTANTS

def create_env(env):
    if env == "Grid":
        return Grid.GridEnv(GRID_CONSTANTS.SCREEN_WIDTH, GRID_CONSTANTS.SCREEN_HEIGHT, GRID_CONSTANTS.SCREEN_TITLE)
    elif env == "Angular":
        return Angular.AngularEnv(ANGULAR_CONSTANTS.SCREEN_WIDTH, ANGULAR_CONSTANTS.SCREEN_HEIGHT, ANGULAR_CONSTANTS.SCREEN_TITLE)
    else:
        raise ValueError("Invalid env name")

def grid_to_abs_pos(val):
    x = int(val[0]) * (GRID_CONSTANTS.WIDTH + GRID_CONSTANTS.MARGIN) + (GRID_CONSTANTS.WIDTH / 2 + GRID_CONSTANTS.MARGIN)
    y = int(val[1]) * (GRID_CONSTANTS.HEIGHT + GRID_CONSTANTS.MARGIN) + (GRID_CONSTANTS.HEIGHT / 2 + GRID_CONSTANTS.MARGIN)
    return x, y

def abs_to_grid_pos(val):
    x = (val[0] - (GRID_CONSTANTS.WIDTH / 2 + GRID_CONSTANTS.MARGIN))// (GRID_CONSTANTS.WIDTH + GRID_CONSTANTS.MARGIN)
    y = (val[1] - (GRID_CONSTANTS.HEIGHT / 2 + GRID_CONSTANTS.MARGIN))// (GRID_CONSTANTS.HEIGHT + GRID_CONSTANTS.MARGIN)
    return x, y