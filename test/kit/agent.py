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

        if (obs[self.player]['resetting']):
            return { 'turn': 0 }

        if (iter == 0 and curr_step == 0):
            self.num = obs[self.player]['player_num']

        me_obs = obs[self.player]
        board_obs = obs['board']


        direction = me_obs['direction']
        head = me_obs['head']
        energy = me_obs['energy']
        speed = me_obs['speed']

        board = np.array(board_obs['board_state'])
        player_owned = np.array(board_obs['players_state'])

        occupied_territory = np.where(np.logical_and(board != PASSED, player_owned == self.num))
        print(direction, len(occupied_territory[0]), file=sys.stderr)

        turn = 1 if iter % 10 == 0 and iter != 0 else 0

        action = {
            'turn': turn
        }

        return action
