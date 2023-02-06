import numpy as np
import sys
class Agent():
    def __init__(self, player: str) -> None:
        self.player = player
        np.random.seed(0)
        self.moves_made = 0

    def act(self, iter: int, curr_step: int, obs, remainingOverageTime: int = 60):

        obs, rewards, dones, infos = obs
        if obs['player_1']['resetting']:
            print(obs['player_1'], file=sys.stderr)

        if (obs['player_0']['speed'] <= curr_step):
            return { 'turn' : 0 }
        
        direction = 0
        if self.moves_made < 2:
            direction = -1
        elif self.moves_made == 40 or self.moves_made == 60:
            direction = -1
        else:
            direction = 0

        action = {
            'turn': direction
        }
        self.moves_made += 1
        return action
