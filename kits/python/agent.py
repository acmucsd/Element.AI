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

        # if resetting, don't waste time
        if (obs[self.player]['resetting']):
            return { 'turn': 0 }

        # if first iteration, save constant observations
        # like player_num
        if (iter == 0 and curr_step == 0):
            self.num = obs[self.player]['player_num']

        # separate player observation from board observation
        me_obs = obs[self.player]
        board_obs = obs['board']


        # collection essential player info
        direction = me_obs['direction']
        head = me_obs['head']
        energy = me_obs['energy']
        speed = me_obs['speed']


        # save arrays which describe board state to numpy arrays for processing
        board = np.array(board_obs['board_state'])
        player_owned = np.array(board_obs['players_state'])


        # simple action: turn every 10 iterations
        turn = 1 if iter % 10 == 0 and iter != 0 else 0
        action = {
            'turn': turn
        }

        # note action should be a dict with action['turn'] = -1, 0, or 1
        return action
