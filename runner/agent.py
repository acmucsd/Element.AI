import numpy as np
import sys
class Agent():
    def __init__(self, player_id) -> None:

        self.player_id = player_id

    def act(self):

        # simple turning algo
        # -1 = turn left, 0 = straight, 1 = turn right
        direction = self.step % 3 - 1
        return direction
