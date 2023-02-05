import random
from .utils import *
from .constants import *


class Player:
    def __init__(self, x, y, player_num):

        self.num = player_num
        self.respawning = False
        self.dead = False

        """ Player Movement Location """
        self.direction = 0 #random.randrange(0,4) # pick a random starting direction
        self.reset = False
        self.last_unoccupied = False

        """ Player Territory Information """
        self.pos = (x, y)
        self.path = set()
        self.zone = set()

        """ Player Score """
        self.score = 0

    def update(self, turn):

        self.direction += turn
        self.direction %= len(DIRECTIONS)

        x = self.pos[0] + DIRECTIONS[self.direction][0]
        y = self.pos[1] + DIRECTIONS[self.direction][1]

        self.pos = (x, y)

    def reset_player(self):
        self.direction = 0
        self.reset = True
