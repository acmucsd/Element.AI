import numpy as np
import sys


# -----------------------------------
# USEFUL CONSTANTS

TEMP = -1
UNOCCUPIED = 0
TAIL = 1
TERRITORY = 2
BOMB = 3
BOOST = 4

# -----------------------------------

class Agent():
    def __init__(self, player: str) -> None:
        self.player = player
        self.times_moved = 0

    def formatAction(self, turn: int):
        return { 'turn': turn }

    def act(self, iter: int, curr_step: int, obs, remainingOverageTime: int = 60):

        # get all info; note: _dones and _infos are irrelevant here
        obs, rewards, _dones, _infos = obs

        # if not allowed to move, don't waste time computing
        if (obs[self.player]['resetting']):
            return self.formatAction(0)

        # if first iteration, save constant observations like player_num
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
        turn = 1 if self.times_moved % 10 == 0 and iter != 0 else 0
        
        # increment steps
        self.times_moved += 1

        # note action should be a dict with action['turn'] = -1, 0, or 1
        return self.formatAction(turn)
