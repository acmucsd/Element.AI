import numpy as np
import sys
class Agent():
    def __init__(self, player: str) -> None:
        self.player = player
        np.random.seed(0)

    def act(self, step: int, obs, remainingOverageTime: int = 60):
        direction = step % 3 - 1

        action = {
            'turn': direction
        }

        return action
