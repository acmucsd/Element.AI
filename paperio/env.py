from pettingzoo import ParallelEnv
from pettingzoo.utils import wrappers

from typing import Any, Dict, Iterable, Iterator, List, Optional, Tuple, TypeVar

import gymnasium.spaces
from gym import spaces
import numpy as np
import random
import collections

from .config import EnvConfig
from .player import Player
from .constants import *

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

        self.setup()

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
        self.grid = np.zeros((map_size, map_size))
        self.player_grid = np.full((map_size, map_size), None)
        
        for player_num in range(self.num_agents):
            start_x, start_y = self.starting_coords[player_num]
            player = Player(start_x, start_y, player_num)
            self.player_dict[self.agents[player_num]] = player
            c, r = player.pos
            for cc in range(c-1, c + 2):
                for rr in range(r-1, r + 2):
                    self.grid[rr][cc] = OCCUPIED
                    self.player_grid[rr][cc] = player
                    player.push_zone((rr, cc))

        self.place_boost_bomb()


    # TODO: Medium Priority
    # seed-based bomb and boost placement (deterministic env)
    # TODO: Medium Priority
    # Smarter boost and bomb placement
    # Essentially tweak algo to have ideal # of bombs and boosts in good locations
    def place_boost_bomb(self):

        map_size = self.env_cfg.map_size
        boost_count = self.env_cfg.boost_count
        bomb_count = self.env_cfg.bomb_count

        # place boosts
        while (boost_count>0):
            x = random.randrange(0, map_size)
            y = random.randrange(0, map_size)
            if(self.grid[x][y]==0):
                self.grid[x][y]= BOOST
                boost_count-=1

        # place bombs
        while (bomb_count>0):
            x = random.randrange(0, map_size)
            y = random.randrange(0, map_size)
            if(self.grid[x][y]==0):
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
            # TODO: High Priority
            # need to convert code so that self.player_grid contains the player_nums, not the player objects
            # "players_state": self.player_grid,
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

    def step(self, actions: ActionDict, initialRound=True):
        """Receives a dictionary of actions keyed by the agent name.

        Returns the observation dictionary, reward dictionary, terminated dictionary, truncated dictionary
        and info dictionary, where each dictionary is keyed by the agent.
        """
        players_moving = []

        for agent in actions.keys():
            action = actions[agent]

            if (True):
                turn = action['turn']
                player: Player = self.player_dict[agent] 

                player.update(turn)
                players_moving.append(player)

        # TODO: Low priority
        # Note that much of the code below is checking edge cases that only arose in GridEnvV1
        # due to the clock-based system used in arcade
        # It shouldn't be a problem, but may come up in testing, and should be cleaned eventually
        # for performance improvements
        for x in players_moving:
            player: Player = x

            if initialRound and player.reset:
                self.reset_player(player)
            elif (player.reset):
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
                        # TODO: Speed algo
                        # player.movement_speed+=1
                    else:
                        raise Exception("Unknown grid value")
        
        self.env_steps += 1
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
            rewards[agent] = len(player.zone)
            dones[agent] = env_done
            infos[agent] = None

        observations['board'] = {
            'iteration': self.env_steps,
            # 'board_state': self.grid,
            # TODO: High Priority
            # need to convert code so that self.player_grid contains the player_nums, not the player objects
            # "players_state": self.player_grid,
        }

        return observations, rewards, dones, infos
        

    # TODO: High Priority
    # Have game run continuously and only end when hit max_iterations
    # This includes respawn functionality
    def reset_player(self, player: Player):
        indices = np.where(self.player_grid == player)

        for i in range(len(indices[0])):
            x = indices[0][i]
            y = indices[1][i]
            self.grid[x][y] = UNOCCUPIED
            self.player_grid[x][y] = None

        player.reset_player()

    def update_occupancy(self, player):

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
                    player.push_zone((c,r))
                elif cell == -1:
                    self.grid[r][c] = UNOCCUPIED
                    self.player_grid[r][c] = None

    # TODO
    def reset(
        self,
        seed: Optional[int] = None,
        return_info: bool = False,
        options: Optional[dict] = None,
    ) -> ObsDict:
        self.setup()

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
            rewards[agent] = len(player.zone)
            dones[agent] = False
            infos[agent] = None

        observations['board'] = {
            'iteration': self.env_steps,
            # 'board_state': self.grid,
            # TODO: High Priority
            # need to convert code so that self.player_grid contains the player_nums, not the player objects
            # "players_state": self.player_grid,
        }

        return observations
    

    # NOTE: seed will be useful only when we implement seed-based bomb/boost placement
    # def seed(self, seed=None):
    #     """Reseeds the environment (making the resulting environment deterministic)."""
    #     raise NotImplementedError(
    #         "Calling seed externally is deprecated; call reset(seed=seed) instead"
    #     )

    # TODO: medium priority
    # add mode='rgb_array' support
    # TODO: very low priority
    # add mode='human' support (pygame)
    # def render(self, mode='rgb_array'):
    #     """Renders the environment as specified by self.render_mode.

    #     Render mode can be `human` to display a window.
    #     Other render modes in the default environments are `'rgb_array'`
    #     which returns a numpy array and is supported by all environments outside of classic,
    #     and `'ansi'` which returns the strings printed (specific to classic environments).
    #     """
    #     raise NotImplementedError

    # NOTE: only necessary if we implement pygame for render(mode='human')
    # def close(self):
    #     """Closes the rendering window."""
    #     pass

    # NOTE: seems redundant, all board info already given to agent in observe()
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