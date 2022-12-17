import numpy as np
import random
import collections
from .player import Player
from .constants import *
from .utils import *

import json
from json import JSONEncoder

from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional, Tuple

@dataclass
class EnvConfig:
    players: List[str]
    rows: int
    cols: int
    max_iterations: int

class GridEnvV2:
    def __init__(self, cfg: EnvConfig):

        self.cfg = cfg
        self.iteration = 0
        self.num_players = len(cfg.players)
        self.grid = np.zeros((cfg.rows, cfg.cols))
        self.player_grid = np.full((cfg.rows, cfg.cols), None)
        self.player_dict = {}

        # TODO smarter spawning
        self.starting_coords = [
            (int(cfg.rows/4), int(cfg.cols/4)),
            (int(cfg.rows/4), int(cfg.cols/4)*3),
            (int(cfg.rows/4)*3, int(cfg.cols/4)*3),
            (int(cfg.rows/4)*3, int(cfg.cols/4)),
        ]
        
        for player_num in range(self.num_players):
            start_x, start_y = self.starting_coords[player_num]
            player = Player(start_x, start_y, player_num, self.cfg.rows, self.cfg.cols)
            self.player_dict[self.cfg.players[player_num]] = player
            c, r = player.pos
            for cc in range(c-1, c + 2):
                for rr in range(r-1, r + 2):
                    self.grid[rr][cc] = OCCUPIED
                    self.player_grid[rr][cc] = player
                    player.push_zone((rr, cc))

        self.place_boost_bomb()

    # TODO: add to game_data to add useful info
    def get_game_data(self, player_id):
        player = self.player_dict[player_id]
        game_data = {
            "player_info": {
                "player_num": player.num,
                "direction": DIRECTIONS[player.direction],
                "head": player.pos,
                "tail": player.path,
                "zone": player.zone,
                "resetting": player.reset,
            },
            "game_info": {
                "iteration" : self.iteration,
                # "board_state": self.grid,                 # working, commented out to shorten prints
                # "players_state": self.player_grid,        # not working, see the below

                # TODO: High Priority
                # need to convert code so that self.player_grid contains the player_nums, not the player objects
            }
        }

        encoded_game_data = json.dumps(to_json(game_data))

        return encoded_game_data

    def step(self, player_id, direction):
        player = self.player_dict[player_id]

        player.update(direction)

        # TODO: Low priority
        # Note that much of the code below is checking edge cases that only arose in GridEnvV1
        # It shouldn't be a problem, but may come up in testing, and should be cleaned eventually
        if player.reset:
            self.reset_player(player)
        else:
            c, r = player.pos
            player_cell = self.grid[r][c]
            if player_cell == PASSED:
                reset_targets = [p for p in self.player_dict.values() if p.pos == player.pos]
                if len(reset_targets) > 1:
                    for target in reset_targets:
                        self.reset_player(target)
                
                self.reset_player(player)
            elif player_cell == OCCUPIED:
                occupied_by = self.player_grid[r][c]
                if player.last_unoccupied and  occupied_by == player:
                    self.update_occupancy(player)
                    player.last_unoccupied = False
                elif occupied_by != player:
                    occupied_by.pop_zone((r,c))
                    self.grid[r][c] = PASSED
                    self.player_grid[r][c] = player
                    player.last_unoccupied = True
            elif player_cell == UNOCCUPIED:
                self.grid[r][c] = PASSED
                self.player_grid[r][c] = player
                player.push_path((c,r))
                player.last_unoccupied = True
            elif player_cell == BOMB:
                self.reset_player(player)
                self.grid[r][c] = PASSED
                self.player_grid[r][c] = player
            elif player_cell == BOOST:
                self.grid[r][c] = PASSED
                self.player_grid[r][c] = player
                player.push_path((c,r))
                player.last_unoccupied = True
                player.movement_speed+=1
            else:
                raise Exception("Unknown grid value")

    # TODO: Medium Priority
    # Smarter boost and bomb placement
    # Essentially tweak algo to have ideal # of bombs and boosts
    def place_boost_bomb(self, boost_count = BOOST_COUNT, bomb_count=BOMB_COUNT):
        # place boosts
        while (boost_count>0):
            x = random.randrange(0, self.cfg.rows)
            y = random.randrange(0, COLUMN_COUNT)
            if(self.grid[x][y]==0):
                self.grid[x][y]= BOOST
                boost_count-=1

        # place bombs
        while (bomb_count>0):
            x = random.randrange(0, self.cfg.rows)
            y = random.randrange(0, COLUMN_COUNT)
            if(self.grid[x][y]==0):
                self.grid[x][y]= BOMB
                bomb_count-=1

    # TODO: High Priority
    # Have game run continuously and only end when hit max_iterations
    # This includes respawn functionality
    def reset_player(self, player):
        indices = np.where(self.player_grid == player)

        for i in range(len(indices[0])):
            x = indices[0][i]
            y = indices[1][i]
            self.grid[x][y] = UNOCCUPIED
            self.player_grid[x][y] = None

        player.reset_player()

    def update_occupancy(self, player):
        queue = collections.deque([])
        for r in range(self.cfg.rows):
            for c in range(COLUMN_COUNT):
                if (r in [0, self.cfg.rows-1] or c in [0, COLUMN_COUNT-1]) and self.grid[r][c] == UNOCCUPIED:
                    queue.append((r, c))
        while queue:
            r, c = queue.popleft()
            if 0<=r<self.cfg.rows and 0<=c<COLUMN_COUNT and self.grid[r][c] == UNOCCUPIED:
                self.grid[r][c] = TEMP
                queue.extend([(r-1, c),(r+1, c),(r, c-1),(r, c+1)])

        for r in range(self.cfg.rows):
            for c in range(COLUMN_COUNT):
                cell = self.grid[r][c]
                occupied_by = self.player_grid[r][c]
                if (occupied_by == player and cell == PASSED) or cell == UNOCCUPIED:
                    self.grid[r][c] = OCCUPIED
                    self.player_grid[r][c] = player
                    player.push_zone((c,r))
                elif cell == -1:
                    self.grid[r][c] = UNOCCUPIED
                    self.player_grid[r][c] = None