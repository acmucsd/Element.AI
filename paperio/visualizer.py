import pygame
import numpy as np
# pygame.surfarray as surfarray
from pygame.examples.arraydemo import surfdemo_show
import sys
from .constants import *
from arcade import color
class Visualizer:
    def __init__(self, size) -> None:
        # self.screen = pygame.display.set_mode((3*N*game_map.width, N*game_map.height))


        self.block_width = 10;
        self.block_height = 10;
        self.WINDOW_HEIGHT = self.block_height * size;
        self.WINDOW_WIDTH = self.block_width * size;
        self.map_size = size
        # self.screen_size = (size*10, size*10)
        # self.tile_width = min(self.screen_size[0] // size, self.screen_size[1] // size)
        # self.WINDOW_SIZE = (self.tile_width * size, self.tile_width * size)
        # # self.surf = pygame.Surface(self.WINDOW_SIZE)
        # # self.surf.fill([239, 120, 79])
        # # pygame.font.init()
        # # self.screen = None
        self.rgb_array = np.zeros((self.WINDOW_WIDTH,self.WINDOW_HEIGHT, 3), dtype=np.uint8)

        self.bomb_img = pygame.transform.scale(pygame.image.load('bomb1.jpg'), (self.block_width, self.block_height))
        self.boost_img = pygame.transform.scale(pygame.image.load('BOOST2.png'), (self.block_width, self.block_width))

        self.water_img = pygame.transform.scale(pygame.image.load('water3.png'), (self.block_width, self.block_width))
        self.water_img_move = pygame.transform.scale(pygame.image.load('waterMoving.png'), (self.block_width, self.block_width))

        self.fire_img = pygame.transform.scale(pygame.image.load('lavaTexture.png'), (self.block_width, self.block_width))
        self.fire_img_move = pygame.transform.scale(pygame.image.load('lavaTextureMove.png'),
                                                     (self.block_width, self.block_width))

        #self.boost_array = pygame.surfarray.array3d(boost_img)
        self.eps = 0
        #print(self.rgbarray.ndim)
        #smallbomb = self.rgbarray[::2.5, ::2.5]
        #(smallbomb, 'smallbomb')

    def init_window(self):

        pygame.init()
        #pygame.display.init()
        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self. WINDOW_HEIGHT))
        self.screen.fill(color.WHITE)
        #self.draw_grid()
        pygame.display.update()

    # def draw_grid(self):
    #     for x in range(0, self.WINDOW_WIDTH, self.block_width):
    #         for y in range(0, self.WINDOW_HEIGHT, self.block_height):
    #             rect = pygame.Rect(x, y, self.block_width, self.block_height)
    #             pygame.draw.rect(self.screen, color.BLACK, rect, 1)

    def render(self):
        pygame.event.pump()
        pygame.display.update();

    def update_scene(self, grid, player_num_grid):
        # self.player_colors = [
        #         (np.array(color.YELLOW_ORANGE, dtype=np.uint8), np.array(color.SAPPHIRE_BLUE, dtype=np.uint8)),
        #         (np.array(color.HOT_PINK, dtype=np.uint8), np.array(color.SAP_GREEN, dtype=np.uint8)),
        #         (np.array(color.RED_ORANGE, dtype=np.uint8), np.array(color.TEAL, dtype=np.uint8)),
        #         (np.array(color.GOLD, dtype=np.uint8), np.array(color.PURPLE_HEART, dtype=np.uint8)),
        #     ]
        self.player_imgs = [(self.water_img_move, self.water_img),
                            (self.fire_img_move, self.fire_img)
                            ]
        for r in range(self.map_size):
            for c in range(self.map_size):
                x = r * self.block_width
                y = c * self.block_height
                if(x >= self.WINDOW_WIDTH or y >= self.WINDOW_HEIGHT):
                    raise Exception("Out of Bounds Exception")
                rect = pygame.Rect(x, y, self.block_width, self.block_height)
                #pygame.draw.rect(self.screen, color.BLACK, rect, 1)
                #self.screen.blit(self.bomb_img, (x,y))
                if grid[r][c] == UNOCCUPIED:
                    #self.rgb_array[r][c] = WHITE_SMOKE
                    pygame.draw.rect(self.screen, color.WHITE, rect, 0)
                elif grid[r][c] == BOMB:
                    #self.rgb_array[r][c] = BLACK
                    self.screen.blit(self.bomb_img, (x,y))
                elif grid[r][c] == BOOST:
                    #self.rgb_array[r][c] = PURPLE
                    self.screen.blit(self.boost_img, (x,y))
                elif grid[r][c] == PASSED:
                    #self.rgb_array[r][c] = self.player_colors[player_num_grid[r][c]][0]
                    #pygame.draw.rect(self.screen, self.player_colors[player_num_grid[r][c]][0], rect, 0)
                    # pygame.draw.rect(self.screen, color.BLACK, rect, 1)
                    self.screen.blit(self.player_imgs[player_num_grid[r][c]][0], (x,y))
                elif grid[r][c] == OCCUPIED:
                    #self.rgb_array[r][c] = self.player_colors[player_num_grid[r][c]][1]
                    self.screen.blit(self.player_imgs[player_num_grid[r][c]][1], (x,y))
                else:
                    raise Exception("Unknown grid value")
        self.rgb_array = pygame.surfarray.array3d(self.screen)

