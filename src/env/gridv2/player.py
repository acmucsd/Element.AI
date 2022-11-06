import arcade
from .constants import *


class Player(arcade.Sprite):
    """ Player Class """
    def update(self):

        """ Move the player """
        # Move player.
        # Remove these lines if physics engine is moving player.
        self.center_x += self.change_x
        self.center_y += self.change_y

        # Check for out-of-bounds
        if self.left < 0:
            self.left = 0

        elif self.right > SCREEN_WIDTH - 1:
            self.right = SCREEN_WIDTH - 1

        if self.bottom < 0:
            self.bottom = 0

        elif self.top > SCREEN_HEIGHT - 1:
            self.top = SCREEN_HEIGHT - 1