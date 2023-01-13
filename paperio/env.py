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
            (int(map_size/4), int(map_size/4)*3),
            (int(map_size/4)*3, int(map_size/4)*3),
            (int(map_size/4)*3, int(map_size/4)),
        ]

        self.player_dict = dict()
        self.grid = np.zeros((map_size, map_size), dtype=np.uint8)
        self.player_grid = np.full((map_size, map_size), None)
        self.player_num_grid = np.full((map_size, map_size), -1, dtype=np.int8)
        
        for player_num in range(self.num_agents):
            start_x, start_y = self.starting_coords[player_num]
            player = Player(start_x, start_y, player_num)
            self.player_dict[self.agents[player_num]] = player
            self._spawn_player(player)

        self.energies = [0] * self.num_agents
        self.speeds = [1] * self.num_agents

        self.place_boost_bomb()

    def _spawn_player(self, player: Player, respawn=False):

        if (respawn):
            empty = np.where(self.grid == UNOCCUPIED)
            if (len(empty[0]) == 0):
                player.dead = True
                return
            
            choice = random.randrange(0, len(empty[0]))
            player.pos = (empty[0][choice], empty[1][choice])
        
        padding = 0 if respawn else 1

        c, r = player.pos
        for cc in range(c - padding, c + padding + 1):
            for rr in range(r - padding, r + padding + 1):
                self.grid[rr][cc] = OCCUPIED
                self.player_grid[rr][cc] = player
                self.player_num_grid[rr][cc] = player.num
                player.push_zone((rr, cc))


    # TODO: Medium Priority
    # seed-based bomb and boost placement (deterministic env)
    # will also need to handle seed being passed from reset() func
    def place_boost_bomb(self, rate = 1.0):

        map_size = self.env_cfg.map_size
        boost_count = int(self.env_cfg.boost_count * rate)
        bomb_count = int(self.env_cfg.bomb_count * rate)

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
            head=spaces.Box(low=0, high=self.env_cfg.map_size, dtype=int),
            # TODO: High Priority
            # figure out implementation of the below items
            # "tail": player.path,
            # "zone": player.zone,
        )

        obs_space['board'] = spaces.Dict(
            iteration=spaces.Discrete(self.env_cfg.max_episode_length),
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

    def update_speeds(self):
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
        self.update_speeds()
        self.env_steps += 1
        self.place_boost_bomb(rate = 0.1)

        for player_num in range(self.num_agents):
            player: Player = self.player_dict[self.agents[player_num]]
            if (player.respawning and not player.dead):
                self._spawn_player(player, respawn=True)
                player.reset = False
                player.respawning = False

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
                    turn = action['turn']

                player.update(turn)
                players_moving.append(player)

        # TODO: Low priority
        # Note that much of the code below is checking edge cases that only arose in GridEnvV1
        # due to the clock-based system used in arcade
        # It shouldn't be a problem, but may come up in testing, and should be cleaned eventually
        # for performance improvements
        # Also ideally we remove self.player_grid and move to only using self.player_num_grid
        for x in players_moving:
            player: Player = x

            if (player.reset or player.dead):
                player.respawning = True
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
                        occupied_by = self.player_grid[r][c]
                        if player.last_unoccupied and  occupied_by == player:
                            self.update_occupancy(player)
                            player.last_unoccupied = False
                        elif occupied_by != player:
                            occupied_by.pop_zone((r,c))
                            self.grid[r][c] = PASSED
                            self.player_grid[r][c] = player
                            self.player_num_grid[r][c] = player.num
                            player.last_unoccupied = True
                    elif player_cell == UNOCCUPIED:
                        self.grid[r][c] = PASSED
                        self.player_grid[r][c] = player
                        self.player_num_grid[r][c] = player.num
                        player.push_path((c,r))
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

                        if (owned_by_num != player.num and owned_by_num != -1):
                            owned_by: Player = self.player_dict[self.agents[owned_by_num]]
                            owned_by.pop_zone((r,c))

                        self.grid[r][c] = PASSED
                        self.player_grid[r][c] = player
                        self.player_num_grid[r][c] = player.num
                        player.push_path((c,r))
                        player.last_unoccupied = True
                        self.energies[player.num] += 1
                    else:
                        raise Exception("Unknown grid value")
        
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
                'direction': DIRECTIONS[player.direction],
                'resetting': player.reset,
                'head': player.pos,
                # NOTE: see observation_space function
                # "tail": player.path,
                # "zone": player.zone,
            }

            # TODO: High priority
            # Implement rewards and infos discts
            # NOTE: dones is false until hit max_episode_length
            # or until the player is dead (i.e. board full, can't respawn)
            rewards[agent] = len(player.zone)
            dones[agent] = env_done or player.dead
            infos[agent] = None

        observations['board'] = {
            'iteration': self.env_steps,
            'board_state': self.grid,
            "players_state": self.player_num_grid,
        }

        return observations, rewards, dones, infos
        
    def reset_player(self, player: Player):
        indices = np.where(self.player_num_grid == player.num)

        for i in range(len(indices[0])):
            x = indices[0][i]
            y = indices[1][i]
            self.grid[x][y] = UNOCCUPIED
            self.player_grid[x][y] = None
            self.player_num_grid[x][y] = -1

        self.energies[player.num] = 0
        player.moves_left = 0

        player.reset_player()

    def update_occupancy(self, player: Player):

        map_size = self.env_cfg.map_size

        queue = collections.deque([])
        for r in range(map_size):
            for c in range(map_size):
                if (r in [0, map_size-1] or c in [0, map_size-1]) and self.grid[r][c] == UNOCCUPIED:
                    queue.append((r, c))
        while queue:
            r, c = queue.popleft()
            if 0<=r<map_size and 0<=c<map_size and self.grid[r][c] == UNOCCUPIED:
                self.grid[r][c] = TEMP
                queue.extend([(r-1, c),(r+1, c),(r, c-1),(r, c+1)])

        for r in range(map_size):
            for c in range(map_size):
                cell = self.grid[r][c]
                occupied_by = self.player_grid[r][c]
                if (occupied_by == player and cell == PASSED) or cell == UNOCCUPIED:
                    self.grid[r][c] = OCCUPIED
                    self.player_grid[r][c] = player
                    self.player_num_grid[r][c] = player.num
                    player.push_zone((c,r))
                elif cell == -1:
                    self.grid[r][c] = UNOCCUPIED
                    self.player_grid[r][c] = None
                    self.player_num_grid[r][c] = -1

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
        
        
    # TODO: high priority
    # make mode='rgb_array' more efficient
    # add mode='human' support (pygame -- see luxai2022 comp for an example)
    def _init_render(self):
        if self.py_visualizer is None:
            self.py_visualizer = Visualizer(self.env_cfg.map_size)
            return True
        return False

    def render(self, mode='rgb_array', skip_update=False):

        if (mode == 'human'):
            if self._init_render():
                self.py_visualizer.init_window()

            if (not skip_update): self.py_visualizer.update_scene(self.grid, self.player_num_grid)
            self.py_visualizer.render()
        

        elif (mode == 'rgb_array'):
            if (skip_update):
                return self.py_visualizer.rgb_array
            else:
                return self.py_visualizer.update_scene(self.grid,self.player_num_grid)

    def close(self):
        """Closes the rendering window."""
        import pygame
        pygame.display.quit()
        pygame.quit()

    # NOTE: seems redundant, all necessary board info already given to agent in observe()
    # def state(self) -> np.ndarray:
    #     """Returns the state.

    #     State returns a global view of the environment appropriate for
    #     centralized training decentralized execution methods like QMIX
    #     """
    #     raise NotImplementedError(
    #         "state() method has not been implemented in the environment {}.".format(
    #             self.metadata.get("name", self.__class__.__name__)
    #         )
    #     )


    
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