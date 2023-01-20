import pygame
import numpy as np
# pygame.surfarray as surfarray
from pygame.examples.arraydemo import surfdemo_show
import sys
from .constants import *

class Visualizer:
    def __init__(self, size) -> None:
        # self.screen = pygame.display.set_mode((3*N*game_map.width, N*game_map.height))
        self.map_size = size
        self.screen_size = (size*10, size*10)
        self.tile_width = min(self.screen_size[0] // size, self.screen_size[1] // size)
        self.WINDOW_SIZE = (self.tile_width * size, self.tile_width * size)
        self.surf = pygame.Surface(self.WINDOW_SIZE)
        self.surf.fill([239, 120, 79])
        pygame.font.init()
        self.screen = None
        self.rgb_array = np.zeros((self.WINDOW_SIZE[0],self.WINDOW_SIZE[1], 3), dtype=np.uint8)

        bomb_img = pygame.transform.scale(pygame.image.load('bomb1.jpg'), (self.tile_width, self.tile_width))
        self.bomb_array = pygame.surfarray.array3d(bomb_img)

        boost_img = pygame.transform.scale(pygame.image.load('BOOST1.png'), (self.tile_width, self.tile_width))
        self.boost_array = pygame.surfarray.array3d(boost_img)
        self.eps = 0
        #print(self.rgbarray.ndim)
        #smallbomb = self.rgbarray[::2.5, ::2.5]
        #(smallbomb, 'smallbomb')

    def init_window(self):

        pygame.init()
        pygame.display.init()
        self.screen = pygame.display.set_mode(self.WINDOW_SIZE)


    def render(self):
        #fStack = np.hstack((self.rgbarray, self.rgbarray, self.rgbarray, self.rgbarray))
        #self.surf = pygame.surfarray.make_surface(np.vstack((fStack, fStack, fStack, fStack)))
        self.surf = pygame.surfarray.make_surface(self.rgb_array)
        pygame.event.pump()
        #self.surf = pygame.surfarray.make_surface(smallbomb)
        #self.surf = pygame.surfarray.array3d(bombimg)
        #imgsurface = pygame.image.load('bomb.jpg')
        #rgbarray = pygame.surfarray.array3d(imgsurface)
        #pygame.examples.surfdemo_show(rgbarray, 'rgbarray')
        #pygame.display.update()
        #resized = pygame.transform.scale(self.surf, self.screen.get_rect().size)
        self.screen.blit(self.surf, (0, 0))
        print('updateScene ' + str(self.eps))
        self.eps += 1
        pygame.display.update()

    def update_block(self, img, row, col):
        for r in range(self.tile_width):
            for c in range(self.tile_width):
                self.rgb_array[row+r][col+c] = img[r][c]

    def update_color(self, color, row, col):
        for r in range(self.tile_width):
            for c in range(self.tile_width):
                self.rgb_array[row+ r][col + c] = color

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
        #print(self.map_size)
        for r in range(self.map_size):
            #row = np.empty((0,0,0))
            for c in range(self.map_size):
                if grid[r][c] == UNOCCUPIED:
                    #self.rgb_array[r][c] = WHITE_SMOKE
                    self.update_color(WHITE_SMOKE, r*self.tile_width, c*self.tile_width)
                elif grid[r][c] == BOMB:
                    #self.rgb_array[r][c] = BLACK
                    self.update_block(self.bomb_array, r*self.tile_width, c*self.tile_width)
                elif grid[r][c] == BOOST:
                    #self.rgb_array[r][c] = PURPLE
                    self.update_block(self.boost_array, r*self.tile_width, c*self.tile_width)
                elif grid[r][c] == PASSED:
                    #self.rgb_array[r][c] = self.player_colors[player_num_grid[r][c]][0]
                    self.update_color(self.player_colors[player_num_grid[r][c]][0], r*self.tile_width, c*self.tile_width)
                elif grid[r][c] == OCCUPIED:
                    #self.rgb_array[r][c] = self.player_colors[player_num_grid[r][c]][1]
                    self.update_color(self.player_colors[player_num_grid[r][c]][1], r*self.tile_width, c*self.tile_width)
                else:
                    raise Exception("Unknown grid value")

                #r += self.tile_width
            #c += self.tile_width
            #np.vstack((self.rgb_array,row))
        #print("running")

        return self.rgb_array
        # fStack = np.hstack((self.rgbarray,self.rgbarray,self.rgbarray,self.rgbarray))
        # return np.vstack((fStack, fStack, fStack, fStack))

