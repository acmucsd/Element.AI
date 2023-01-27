import numpy as np
import sys
class Agent():
    def __init__(self, player: str) -> None:
        self.player = player
        np.random.seed(0)
        self.moves_made = 0

    def act(self, iter: int, curr_step: int, obs, remainingOverageTime: int = 60):

        obs, rewards, dones, infos = obs
        if self.moves_made == 4:
            direction = -1
        else:
            direction = 0
        if obs['player_1']['resetting']:
            print(obs['player_1'], file=sys.stderr)

        # result = [obs['player_1']['head'][0] + obs['player_1']['direction'][0], obs['player_1']['head'][1] + obs['player_1']['direction'][1]]
        # if result[0] > 99 or result[1] > 99 or result[0] < 0 or result[1] < 0:
        #     direction = -1
        # else:
        #     direction = 0

        action = {
            'turn': direction
        }
        self.moves_made += 1
        return action
