""" Agent Values """
DIRECTIONS = ((0,1), (1,0), (0,-1), (-1,0))
VALID_MOVES = (-1, 0, 1)

""" Environment Values """
ROW_COUNT = 80
COLUMN_COUNT = 80

""" Tile Values """
TEMP = -1
UNOCCUPIED = 0
PASSED = 1
OCCUPIED = 2
BOMB = 3
BOOST = 4

""" Rendering Values """
SPRITE_SCALING = 0.5
WIDTH = 10
HEIGHT = 10
MARGIN = 5
SCREEN_WIDTH = (WIDTH + MARGIN) * COLUMN_COUNT + MARGIN
SCREEN_HEIGHT = (HEIGHT + MARGIN) * ROW_COUNT + MARGIN
SCREEN_TITLE = "Paper IO Game"

""" Colors """
COLORS = [
    ([243,77,5], [104,33,2]),
    ([83, 216, 185], [35,174,186]),
    ([116, 62, 12], [70, 46, 26]),
    ([146, 211, 254], [244, 231, 236]),
]

import numpy as np
WHITE_SMOKE = np.array([245] * 3)
BLACK = np.array([0] * 3)
PURPLE = np.array([175, 100, 255])

PLAYER_HEAD_COLOR = np.array([88] * 3)

PLAYER_COLORS = []
for color_pair in COLORS:
  PLAYER_COLORS.append((np.array(color_pair[0]), np.array(color_pair[1])))