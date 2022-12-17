import numpy as np
import sys
class Agent():
    def __init__(self, player) -> None:
        self.player = player
        self.step = 0

    def early_setup(self):
        direction = 0
        return direction
        

    def act(self):
        direction = self.step % 3 - 1
        return direction
