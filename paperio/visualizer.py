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

    def update_scene(self, grid, player_num_grid, num_agents, player_dict: dict):
        grid = np.transpose(grid)
        player_num_grid = np.transpose(player_num_grid)
        for i in range(num_agents):
            self.rgb_array[np.logical_and(grid == PASSED, player_num_grid == i)] = PLAYER_COLORS[i][0]
            self.rgb_array[np.logical_and(grid == OCCUPIED, player_num_grid == i)] = PLAYER_COLORS[i][1]
        for player in player_dict.values():
            self.rgb_array[player.pos] = PLAYER_HEAD_COLOR
        self.rgb_array[grid == UNOCCUPIED] = WHITE_SMOKE
        self.rgb_array[grid == BOMB] = BLACK
        self.rgb_array[grid == BOOST] = PURPLE
