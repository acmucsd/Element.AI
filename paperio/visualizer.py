import pygame
import numpy as np
from .constants import *

class Visualizer:
    def __init__(self, size) -> None:
        # self.screen = pygame.display.set_mode((3*N*game_map.width, N*game_map.height))
        self.map_size = size
        self.screen_size = (size*4, size*4)
        self.tile_width = min(self.screen_size[0] // size, self.screen_size[1] // size)
        self.WINDOW_SIZE = (self.tile_width * size, self.tile_width * size)
        self.surf = pygame.Surface(self.WINDOW_SIZE)
        self.surf.fill([239, 120, 79])
        pygame.font.init()
        self.screen = None
        self.rgb_array = np.zeros((self.map_size, self.map_size, 3), dtype=np.uint8)

    def init_window(self):
        pygame.init()
        pygame.display.init()
        self.screen = pygame.display.set_mode(self.WINDOW_SIZE)


    def render(self):
        self.surf = pygame.surfarray.make_surface(self.rgb_array)
        pygame.display.update()
        resized = pygame.transform.scale(self.surf, self.screen.get_rect().size)
        self.screen.blit(resized, (0, 0))

    def update_scene(self, grid, player_num_grid):
        from arcade import color

        self.rgb_array = np.zeros((self.map_size, self.map_size, 3), dtype=np.uint8)

        self.player_colors = [
                (np.array(color.YELLOW_ORANGE, dtype=np.uint8), np.array(color.SAPPHIRE_BLUE, dtype=np.uint8)),
                (np.array(color.HOT_PINK, dtype=np.uint8), np.array(color.SAP_GREEN, dtype=np.uint8)),
                (np.array(color.RED_ORANGE, dtype=np.uint8), np.array(color.TEAL, dtype=np.uint8)),
                (np.array(color.GOLD, dtype=np.uint8), np.array(color.PURPLE_HEART, dtype=np.uint8)),
            ]

        WHITE_SMOKE = np.array(color.WHITE_SMOKE)
        BLACK = np.array(color.BLACK)
        PURPLE = np.array(color.PURPLE)

        for r in range(self.map_size):
            for c in range(self.map_size):
                if grid[r][c] == UNOCCUPIED:
                    self.rgb_array[r][c] = WHITE_SMOKE
                elif grid[r][c] == BOMB:
                    self.rgb_array[r][c] = BLACK
                elif grid[r][c] == BOOST:
                    self.rgb_array[r][c] = PURPLE
                elif grid[r][c] == PASSED:
                    self.rgb_array[r][c] = self.player_colors[player_num_grid[r][c]][0]
                elif grid[r][c] == OCCUPIED:
                    self.rgb_array[r][c] = self.player_colors[player_num_grid[r][c]][1]
                else:
                    raise Exception("Unknown grid value")
