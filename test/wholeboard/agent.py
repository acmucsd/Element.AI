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
        self.last_reward = -1
        np.random.seed(0)
        self.steps = 0

    def act(self, iter: int, curr_step: int, obs, remainingOverageTime: int = 60):

        obs, rewards, dones, infos = obs

        # if resetting, don't waste time
        if (obs[self.player]['resetting']):
            # note we still return a valid action, else the env will log the errors
            # and clutter up the console
            return { 'turn': 0 }

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

        # if first iteration, save constant observations
        # like player_num
        if (iter == 0 and curr_step == 0):
            self.num = obs[self.player]['player_num']
            self.map_size = board.shape[0]

        # turn right if about to die
        turn = 0
        x, y = head
        x_dir, y_dir = direction
        next_x, next_y = x + x_dir, y + y_dir
        if (next_x == -1 or self.map_size <= next_x or next_y == -1 or self.map_size <= next_y):
            turn = 1
        elif (board[next_y,next_x] == PASSED):
            turn = 1

        action = {
            'turn': turn
        }
        # note action should be a dict with action['turn'] = -1, 0, or 1
        return action