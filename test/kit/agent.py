import numpy as np
import sys

TEMP = -1
UNOCCUPIED = 0
PASSED = 1
OCCUPIED = 2
BOMB = 3
BOOST = 4
class Agent():
    def __init__(self, player: str) -> None:
        self.player = player
        np.random.seed(0)

    def act(self, iter: int, curr_step: int, obs, remainingOverageTime: int = 60):

        obs, rewards, dones, infos = obs

        self_obs = obs[self.player]
        player_num = self_obs['player_num']
        head = self_obs['head']
        direction = self_obs['direction']

        board_obs = obs['board']
        board = np.array(board_obs['board_state'])
        player_owned = np.array(board_obs['players_state'])

        occupied_territory = np.where(np.logical_and(board != PASSED, player_owned == player_num))
        print(direction, len(occupied_territory[0]), file=sys.stderr)

        direction = 0
        if iter % 10 == 0 and iter != 0: direction = 1

        action = {
            'turn': direction
        }

        return action
