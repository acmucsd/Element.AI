import random
from .utils import *
from .constants import *


class Player:
    def __init__(self, x, y, player_num, map_size):

        self.num = player_num

        """ Player Movement Location """
        self.direction = 0 #random.randrange(0,4) # pick a random starting direction
        self.reset = False
        self.last_unoccupied = False

        """ Player Territory Information """
        self.pos = (x, y)
        self.path = set()
        self.zone = set()

        """ Player Score """
        self.score = -1

        """ Game-Related Values """
        self.map_size = map_size

    def update(self, direction):

        self.direction += direction
        self.direction %= len(DIRECTIONS)

        x = self.pos[0] + DIRECTIONS[self.direction][0]
        y = self.pos[1] + DIRECTIONS[self.direction][1]

        self.pos = (x, y)
        if x < 0 or x>= self.map_size or y < 0 or y>=self.map_size:
            self.reset = True

    def pop_zone(self, pos):
        self.zone.discard(pos)
    def push_zone(self, pos):
        self.zone.add(pos)
        self.path.discard(pos)

    def push_path(self, pos):
        if pos not in self.zone: self.path.add(pos)

    def reset_player(self):
        self.reset = True
        self.score = len(self.zone)
        self.stopped = True