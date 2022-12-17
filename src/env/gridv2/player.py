import random
from .utils import *
from .constants import *


class Player:
    def __init__(self, x, y, player_num):

        self.num = player_num

        """ Player Movement Location """
        self.movement_speed = 10 # need to adjust it to scale or something
        self.center_x, self.center_y = grid_to_abs_pos((x,y))
        self.actual_x = self.center_x
        self.actual_y = self.center_y
        self.direction = 0 #random.randrange(0,4) # pick a random starting direction
        self.reset=False
        self.last_unoccupied = False

        """ Player Territory Information """
        self.pos = (x, y)
        self.path = set()
        self.zone = set()

        """ Player Score """
        self.score = -1

    def snap(self):
        x, y = abs_to_grid_pos((self.actual_x, self.actual_y))
        self.center_x, self.center_y = grid_to_abs_pos((x,y))
        self.pos = (int(x), int(y))

    def update(self, direction):

        self.direction += direction
        self.direction = (self.direction+4) % len(DIRECTIONS)

        self.old_pos = self.pos
        self.old_path = self.path
        self.old_zone = self.zone

        self.actual_x += DIRECTIONS[self.direction][0]*self.movement_speed
        self.actual_y += DIRECTIONS[self.direction][1]*self.movement_speed
        # print(self.pos)
        self.snap()
        # print(self.pos)

        x,y = self.pos
        if x < 0 or x>= ROW_COUNT or y < 0 or y>=COLUMN_COUNT:
            self.reset = True

    def pop_zone(self, pos):
        self.zone.discard(pos)
    def push_zone(self, pos):
        self.zone.add(pos)
        self.path.discard(pos)

    def push_path(self, pos):
        if pos not in self.zone: self.path.add(pos)

    def valid_collision(self):
        if (self.old_pos == self.pos):
            return False
        return True

    def reset_player(self):
        self.reset = True
        self.score = len(self.zone)
        self.stopped = True