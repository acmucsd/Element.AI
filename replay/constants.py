import numpy as np

# Constants
TEMP, UNOCCUPIED, PASSED, OCCUPIED, BOMB, BOOST = -1, 0, 1, 2, 3, 4

COLORS = [
    ([243,77,5], [104,33,2]),
    ([83, 216, 185], [35,174,186]),
    ([116, 62, 12], [70, 46, 26]),
    ([146, 211, 254], [244, 231, 236]),
]

WHITE_SMOKE = np.array([245] * 3)
BLACK = np.array([0] * 3)
PURPLE = np.array([175, 100, 255])

PLAYER_HEAD_COLOR = np.array([88] * 3)

PLAYER_COLORS = []
for color_pair in COLORS:
    PLAYER_COLORS.append((np.array(color_pair[0]), np.array(color_pair[1])))