import numpy as np
import sys
class Agent():
    def __init__(self, player: str) -> None:
        self.player = player
        np.random.seed(0)
        self.moves_made = 0

    def act(self, iter: int, curr_step: int, obs, remainingOverageTime: int = 60):

        obs, rewards, dones, infos = obs
        result = [obs['player_0']['head'][0] + obs['player_0']['direction'][0], obs['player_0']['head'][1] + obs['player_0']['direction'][1]]
        if obs['player_0']['resetting']:
            print(obs['player_0'], file=sys.stderr)

        if self.moves_made == 10 or self.moves_made == 40 or self.moves_made == 50:
            direction = 1
            # print(direction, file=sys.stderr)
        else:
            direction = 0

        action = {
            'turn': direction
        }
        self.moves_made += 1

        return action
