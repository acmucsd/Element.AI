from lux.kit import obs_to_game_state, GameState, EnvConfig
from lux.utils import direction_to, my_turn_to_place_factory
import numpy as np
import sys
class Agent():
    def __init__(self, player: str, env_cfg: EnvConfig) -> None:
        self.player = player
        np.random.seed(0)
        self.env_cfg: EnvConfig = env_cfg

    def act(self, step: int, obs, remainingOverageTime: int = 60):
        direction = step % 3 - 1

        action = {
            'turn': direction
        }

        return action
