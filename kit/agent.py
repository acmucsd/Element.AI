import numpy as np
import sys
class Agent():
    def __init__(self, player: str) -> None:
        self.player = player
        np.random.seed(0)

    def act(self, iter: int, curr_step: int, obs, remainingOverageTime: int = 60):

        direction = iter % 3 - 1

        print(iter, curr_step, file=sys.stderr)

        action = {
            'turn': direction
        }

        return action
