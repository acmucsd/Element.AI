from pettingzoo import ParallelEnv
from pettingzoo.utils import wrappers

from typing import Any, Dict, Iterable, Iterator, List, Optional, Tuple, TypeVar

import gymnasium.spaces
from gym import spaces
import numpy as np
import random
import collections
import sys
from arcade import color

from .config import EnvConfig
from .player import Player
from .constants import *
from .visualizer import Visualizer

ObsType = TypeVar("ObsType")
ActionType = TypeVar("ActionType")
AgentID = str

ObsDict = Dict[AgentID, ObsType]
ActionDict = Dict[AgentID, ActionType]

def env():
    """
    The env function often wraps the environment in wrappers by default.
    You can find full documentation for these methods
    elsewhere in the developer documentation.
    """
    env = raw_env()
    # This wrapper is only for environments which print results to the terminal
    env = wrappers.CaptureStdoutWrapper(env)
    # this wrapper helps error handling for discrete action spaces
    env = wrappers.AssertOutOfBoundsWrapper(env)
    # Provides a wide vareity of helpful user errors
    # Strongly recommended
    env = wrappers.OrderEnforcingWrapper(env)
    return env

class PaperIO(ParallelEnv):
    metadata = {"render.modes": ["human", "rgb_array"], "name": "ACM_AI_SP22_PaperIO.v0"}

    """
    Init Functions
    """

    def __init__(self, **kwargs):

        default_config = EnvConfig(**kwargs)
        self.env_cfg = default_config

        self.possible_agents = ["player_" + str(r) for r in range(self.env_cfg.max_players)]

        self.agents = self.possible_agents[:self.env_cfg.num_players]

        self.max_episode_length = self.env_cfg.max_episode_length

        self.py_visualizer: Visualizer = None

    def setup(self):

        self.env_steps = 0

        # TODO smarter spawning
        map_size = self.env_cfg.map_size
        self.starting_coords = [
            (int(map_size/4), int(map_size/4)),
            (int(map_size/4)*3, int(map_size/4)),
            (int(map_size/4), int(map_size/4)*3),
            (int(map_size/4)*3, int(map_size/4)*3),
        ]

        self.player_dict = dict()
        self.grid = np.zeros((map_size, map_size), dtype=np.int8)
        self.player_num_grid = np.full((map_size, map_size), -1, dtype=np.int8)
        
        for player_num in range(self.num_agents):
            start_x, start_y = self.starting_coords[player_num]
            player = Player(start_x, start_y, player_num)
            self.player_dict[self.agents[player_num]] = player
            self._spawn_player(player)

        self.energies = [0] * self.num_agents
        self.speeds = [1] * self.num_agents

        self._place_boost_bomb(initial_spawn=True)

    def _spawn_player(self, player: Player, respawn=False):

        if (respawn):
            empty = np.where(self.grid == UNOCCUPIED)
            if (len(empty[0]) == 0):
                return
            
            choice = random.randrange(0, len(empty[0]))
            player.pos = (empty[1][choice], empty[0][choice])
        
        padding = 0 if respawn else 1

        c, r = player.pos
        for cc in range(c - padding, c + padding + 1):
            for rr in range(r - padding, r + padding + 1):
                self.grid[rr][cc] = OCCUPIED
                self.player_num_grid[rr][cc] = player.num

    def _place_boost_bomb(self, initial_spawn = False):

        boost_locs = np.where(self.grid == BOOST)
        bomb_locs = np.where(self.grid == BOMB)

        missing_boosts = self.env_cfg.boost_count - len(boost_locs[0])
        missing_bombs = self.env_cfg.bomb_count - len(bomb_locs[0])

        boost_count = min(self.env_cfg.boost_respawn_rate, missing_boosts)
        bomb_count = min(self.env_cfg.bomb_respawn_rate, missing_bombs)

        if (initial_spawn):
            boost_count = int(self.env_cfg.boost_count / 2)
            bomb_count = int(self.env_cfg.bomb_count / 2)

        # place boosts
        while (boost_count>0):
            empty = np.where(np.logical_or(self.grid == UNOCCUPIED, self.grid == OCCUPIED))
            if (len(empty[0])==0):
                return
            choice = random.randrange(0, len(empty[0]))
            x,y = empty[0][choice], empty[1][choice]
            if (x-1 >= 0 and (x-1, y) in self.starting_coords):
                boost_count-=1
            else:
                self.grid[x][y]= BOOST
                boost_count-=1
            
        # place bombs
        while (bomb_count>0):
            empty = np.where(np.logical_or(self.grid == UNOCCUPIED, self.grid == OCCUPIED))
            if (len(empty[0])==0):
                return
            choice = random.randrange(0, len(empty[0]))
            x,y = empty[0][choice], empty[1][choice]
            if (x-1 >= 0 and (x-1, y) in self.starting_coords):
                bomb_count-=1
            else:
                self.grid[x][y]= BOMB
                bomb_count-=1

    """
    Space Functions
    """

    def observation_space(self, agent: AgentID) -> gymnasium.spaces.Space:
        
        obs_space = dict()

        obs_space[agent] = spaces.Dict(
            player_num=spaces.Discrete(self.num_agents),
            direction=spaces.Box(low=-1, high=1, shape=(2,), dtype=int),
            resetting=spaces.Box(low=0, high=1, dtype=bool),
            head=spaces.Box(low=-1, high=self.env_cfg.map_size, dtype=int),
            energy=spaces.Box(low=0, high=1000, dtype=int),
            speed=spaces.Box(low=1, high=5, dtype=int)
        )

        obs_space['board'] = spaces.Dict(
            board_state=spaces.Box(low=0, high=4, shape=self.grid.shape, dtype=self.grid.dtype),
            players_state=spaces.Box(low=-1, high=(self.num_agents-1), shape=self.player_num_grid.shape, dtype=self.player_num_grid.dtype),
        )

        return spaces.Dict(obs_space)

    def action_space(self, agent: str) -> gymnasium.spaces.Space:
        
        act_space = spaces.Dict(
            turn=spaces.Discrete(3, start=-1),
        )

        return act_space

    """
    Env Runtime Functions
    """

    def _update_speeds(self):
        # NOTE: This need to be adjusted once better spawn algo done
        # resultant speeds:
        #               2, 3, 4,  5
        req_energies = [2, 4, 11, 20]

        i = 0
        for energy in self.energies:
            speed = 1
            for req in req_energies:
                if (energy >= req):
                    speed += 1
                else:
                    break
            self.speeds[i] = speed
            i += 1

    def _update_env(self):
        self._update_speeds()
        self.env_steps += 1
        self._place_boost_bomb()

        for player_num in range(self.num_agents):
            player: Player = self.player_dict[self.agents[player_num]]
            if (player.respawning):
                self._spawn_player(player, respawn=True)
                player.reset = False
                player.respawning = False
            player.score += len(np.where(np.logical_and(self.grid != PASSED, self.player_num_grid == player.num))[0])

    def step(self, actions: ActionDict, step_num):
        """Receives a dictionary of actions keyed by the agent name.

        Returns the observation dictionary, reward dictionary, terminated dictionary, truncated dictionary
        and info dictionary, where each dictionary is keyed by the agent.
        """
        players_moving = []

        for agent in actions:
            action = actions[agent]
            player: Player = self.player_dict[agent] 

            if (self.speeds[player.num] > step_num):

                turn = 0

                if (action != None):
                    try:
                        attempted_action = action['turn']
                        if (int(attempted_action) in VALID_MOVES):
                            turn = attempted_action
                    except:
                        pass

                if (not (player.reset)): player.update(turn)
                players_moving.append(player)

        for x in players_moving:
            player: Player = x

            if (player.reset):
                if (step_num == 0): player.respawning = True
                continue
            else:
                c, r = player.pos
                if c < 0 or c>= self.env_cfg.map_size or r < 0 or r>=self.env_cfg.map_size:
                    self.reset_player(player)
                else:
                    player_cell = self.grid[r][c]
                    if player_cell == PASSED:
                        reset_targets = [p for p in self.player_dict.values() if p.pos == player.pos]
                        if len(reset_targets) > 1:
                            for target in reset_targets:
                                self.reset_player(target)
                        
                        self.reset_player(player)
                    elif player_cell == OCCUPIED:
                        occ_num = self.player_num_grid[r][c]
                        if player.last_unoccupied and occ_num == player.num:
                            self.update_occupancy(player)
                            player.last_unoccupied = False
                        elif occ_num != player.num:
                            occupied_by: Player = self.player_dict[self.agents[occ_num]]
                            self.grid[r][c] = PASSED
                            self.player_num_grid[r][c] = player.num
                            player.last_unoccupied = True
                    elif player_cell == UNOCCUPIED:
                        self.grid[r][c] = PASSED
                        self.player_num_grid[r][c] = player.num
                        player.last_unoccupied = True
                    elif player_cell == BOMB:
                        owned_by_num = self.player_num_grid[r][c]

                        if (owned_by_num == -1):
                            self.grid[r][c] = UNOCCUPIED
                        elif (owned_by_num != player.num):
                            self.grid[r][c] = OCCUPIED

                        self.reset_player(player)
                    elif player_cell == BOOST:
                        owned_by_num = self.player_num_grid[r][c]

                        if (owned_by_num != player.num):
                            self.grid[r][c] = PASSED
                            self.player_num_grid[r][c] = player.num
                            player.last_unoccupied = True
                            
                        self.energies[player.num] += 1
                    else:
                        raise Exception("Unknown grid value")

        if (step_num == max(self.speeds) - 1):
            self._update_env()
        
        return self.observe()

    def observe(self):
        env_done = self.env_steps == self.env_cfg.max_episode_length

        observations = dict()
        rewards = dict()
        dones = dict()
        infos = dict()

        for agent in self.agents:
            player:Player = self.player_dict[agent]

            observations[agent] = {
                'player_num': player.num,
                'direction': DIRECTIONS[player.direction] if not player.reset else (-1, -1),
                'resetting': player.reset,
                'head': player.pos,
                'energy': self.energies[player.num],
                'speed': self.speeds[player.num],
            }

            rewards[agent] = player.score
            dones[agent] = env_done
            infos[agent] = None

        observations['board'] = {
            'board_state': np.copy(self.grid),
            "players_state": np.copy(self.player_num_grid),
        }

        return observations, rewards, dones, infos
        
    def reset_player(self, player: Player):
        indices = np.where(self.player_num_grid == player.num)

        for i in range(len(indices[0])):
            x = indices[0][i]
            y = indices[1][i]
            if (self.grid[x][y] not in [BOMB, BOOST]): self.grid[x][y] = UNOCCUPIED
            self.player_num_grid[x][y] = -1

        self.energies[player.num] = 0
        player.pos = (-1, -1)

        player.reset_player()

    def update_occupancy(self, player: Player):
        map_size = self.env_cfg.map_size
        indices = np.moveaxis(np.mgrid[:map_size,:map_size], 0, -1)
        edge = np.concatenate((indices[0,:], indices[map_size-1,:], indices[1:map_size-1,0], indices[1:map_size-1,map_size-1]))

        OCCUPIED_TARGS = [UNOCCUPIED, BOMB, BOOST]

        queue = collections.deque(edge.tolist())
        explored = np.full((map_size, map_size), False)
        while queue:
            r, c = queue.popleft()

            if (0 <= r < map_size and 0 <= c < map_size) and (not explored[r,c]):
                explored[r,c] = True
            
                cell = self.grid[r,c]
                occ_num = self.player_num_grid[r,c]

                if (cell in OCCUPIED_TARGS) or (occ_num != player.num):
                    if cell == UNOCCUPIED:
                        self.grid[r,c] = TEMP
                    elif cell == BOMB:
                        self.grid[r,c] = TEMP * BOMB 
                    elif cell == BOOST:
                        self.grid[r,c] = TEMP * BOOST
                    elif cell == OCCUPIED:
                        self.grid[r,c] = TEMP * OCCUPIED

                    queue.extend([(r-1, c),(r+1, c),(r, c-1),(r, c+1)])

        grid_bomb_or_boost = np.logical_or(self.grid == BOMB, self.grid == BOOST)
        grid_occupied_targ = np.logical_or(self.grid == UNOCCUPIED, grid_bomb_or_boost)
        grid_player_passed = np.logical_and(self.grid == PASSED, self.player_num_grid == player.num)
        enclosed = np.logical_or(grid_player_passed, grid_occupied_targ)
        enclosed_occupied = self.grid == OCCUPIED
        enclosed_unoccupied = np.logical_or(grid_player_passed, self.grid == UNOCCUPIED)

        free_tile = self.grid == TEMP
        free_bomb = self.grid == TEMP * BOMB
        free_boost = self.grid == TEMP * BOOST
        free_occupied = self.grid == TEMP * OCCUPIED

        self.grid[enclosed_unoccupied] = OCCUPIED
        self.player_num_grid[enclosed] = player.num
        self.player_num_grid[enclosed_occupied] = player.num

        self.grid[free_tile] = UNOCCUPIED
        self.grid[free_bomb] = BOMB
        self.grid[free_boost] = BOOST
        self.grid[free_occupied] = OCCUPIED

    def reset(
        self,
        seed: Optional[int] = None,
        return_info: bool = False,
        options: Optional[dict] = None,
    ) -> ObsDict:
        if seed is not None:
            self._seed_run(seed)
        self.setup()

        return self.observe()
    

    def _seed_run(self, seed=None):
        """Reseeds the environment (making the resulting environment deterministic)."""
        np.random.seed(seed)
        random.seed(seed)
        
    def _init_render(self):
        if self.py_visualizer is None:
            self.py_visualizer = Visualizer(self.env_cfg.map_size)
            return True
        return False

    def render(self, mode='rgb_array', skip_update=False):

        if (mode == 'human'):
            if self._init_render():
                self.py_visualizer.init_window()
            if (not skip_update): self.py_visualizer.update_scene(self.grid, self.player_num_grid, self.num_agents, self.player_dict)
            self.py_visualizer.render()
        

        elif (mode == 'rgb_array'):
            self._init_render()
            if (not skip_update): self.py_visualizer.update_scene(self.grid, self.player_num_grid, self.num_agents, self.player_dict)
            return np.copy(self.py_visualizer.rgb_array)

    def close(self):
        """Closes the rendering window."""
        import pygame
        pygame.display.quit()
        pygame.quit()

    # NOTE: seems redundant, all necessary board info already given to agent in observe()
    def state(self) -> np.ndarray:
        """Returns the state.

        State returns a global view of the environment appropriate for
        centralized training decentralized execution methods like QMIX
        """
        raise NotImplementedError(
            "state() method has not been implemented in the environment {}.".format(
                self.metadata.get("name", self.__class__.__name__)
            )
        )


    
    """
    Properties
    """

    @property
    def num_agents(self) -> int:
        return len(self.agents)

    @property
    def max_num_agents(self) -> int:
        return len(self.possible_agents)

    def __str__(self) -> str:
        """Returns the name.

        Which looks like: "space_invaders_v1" by default
        """
        if hasattr(self, "metadata"):
            return self.metadata.get("name", self.__class__.__name__)
        else:
            return self.__class__.__name__

    @property
    def unwrapped(self) -> ParallelEnv:
        return self

def raw_env() -> PaperIO:
    """
    To support the AEC API, the raw_env() function just uses the from_parallel
    function to convert from a ParallelEnv to an AEC env
    """
    env = PaperIO()
    # env = parallel_to_aec(env)
    return env