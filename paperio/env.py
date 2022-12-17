from pettingzoo import AECEnv

import warnings
from typing import Any, Dict, Iterable, Iterator, List, Optional, Tuple, TypeVar

import gymnasium.spaces
from gym import spaces
import numpy as np
import random
import collections

from paperio.config import EnvConfig
from paperio.player import Player
from paperio.constants import *

ObsType = TypeVar("ObsType")
ActionType = TypeVar("ActionType")
AgentID = str

ObsDict = Dict[AgentID, ObsType]
ActionDict = Dict[AgentID, ActionType]

class PaperIO(AECEnv):
    """
    Init Functions
    """

    def __init__(self, **kwargs):

        default_config = EnvConfig(**kwargs)
        self.env_cfg = default_config

        self.possible_agents = ["player_" + str(r) for r in range(self.env_cfg.max_players)]

        self.agents = self.possible_agents
        self.max_episode_length = self.env_cfg.max_episode_length

        self.setup()

        pass

    def setup(self):

        self.iteration = 0
        self.agent_selection_num = 0
        self.agent_selection = self.agents[self.agent_selection_num]

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
            player = Player(start_x, start_y, player_num, map_size)
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
    def observe(self, agent: str):
        player = self.player_dict[agent]

        game_data = {
            agent: {
                'player_num': player.num,
                'direction': DIRECTIONS[player.direction],
                'resetting': player.reset,
                'head': player.pos,
                # NOTE: see observation_space function
                # "tail": player.path,
                # "zone": player.zone,
            },
            'board': {
                'iteration' : self.iteration,
                'board_state': self.grid,
                # NOTE: see observation_space function
                # "players_state": self.player_grid,
            }
        }

        return game_data

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
            turn=spaces.Discrete(3, start=-1)
        )

        return act_space

    def last(self, observe: bool = True):
        """Returns observation, cumulative reward, terminated, truncated, info for the current agent (specified by self.agent_selection)."""
        agent = self.agent_selection
        assert agent
        observation = self.observe(agent) if observe else None
        return (
            observation,
            # self._cumulative_rewards[agent],
            # self.terminations[agent],
            # self.truncations[agent],
            # self.infos[agent],
        )



    """
    Env Runtime Functions
    """

    def step(self, action: ActionType) -> None:
        player = self.player_dict[self.agent_selection]

        turn = action['turn']
        player.update(turn)

        # TODO: Low priority
        # Note that much of the code below is checking edge cases that only arose in GridEnvV1
        # due to the clock-based system used in arcade
        # It shouldn't be a problem, but may come up in testing, and should be cleaned eventually
        # for performance improvements
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

        self.agent_selection_num += 1
        self.agent_selection_num %= self.num_agents

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

    def reset(self, seed: Optional[int] = None, return_info: bool = False, options: Optional[dict] = None) -> None:
        self.setup()

    # TODO: medium priority
    # add mode='rgb_array' support
    # TODO: very low priority
    # add mode='human' support (pygame)
    def render(self, mode='rgb_array'):
        """Renders the environment as specified by self.render_mode.

        Render mode can be `human` to display a window.
        Other render modes in the default environments are `'rgb_array'`
        which returns a numpy array and is supported by all environments outside of classic,
        and `'ansi'` which returns the strings printed (specific to classic environments).
        """
        raise NotImplementedError

    # NOTE: seems redundant, all board info already given to agent in observe()
    # def state(self) -> np.ndarray:
    #     """State returns a global view of the environment.

    #     It is appropriate for centralized training decentralized execution methods like QMIX
    #     """
    #     raise NotImplementedError(
    #         "state() method has not been implemented in the environment {}.".format(
    #             self.metadata.get("name", self.__class__.__name__)
    #         )
    #     )

    # NOTE: only necessary if we implement pygame for render(mode='human')
    # def close(self):
    #     """Closes any resources that should be released.

    #     Closes the rendering window, subprocesses, network connections,
    #     or any other resources that should be released.
    #     """
    #     pass

    # NOTE: seed will be useful only when we implement seed-based bomb/boost placement
    # def seed(self, seed: Optional[int] = None) -> None:
    #     """Reseeds the environment (making the resulting environment deterministic)."""
    #     raise NotImplementedError(
    #         "Calling seed externally is deprecated; call reset(seed=seed) instead"
    #     )

    # NOTE: note useful rn
    # def agent_iter(self, max_iter: int = 2**63) -> AECIterable:
    #     """Yields the current agent (self.agent_selection).

    #     Needs to be used in a loop where you step() each iteration.
    #     """
    #     return AECIterable(self, max_iter)



    """
    Properties
    """

    @property
    def num_agents(self) -> int:
        return len(self.agents)

    @property
    def max_num_agents(self) -> int:
        return len(self.possible_agents)

    @property
    def unwrapped(self) -> AECEnv:
        return self


    
    """
    Rewards
    """

    def _clear_rewards(self) -> None:
        """Clears all items in .rewards."""
        for agent in self.rewards:
            self.rewards[agent] = 0

    def _accumulate_rewards(self) -> None:
        """Adds .rewards dictionary to ._cumulative_rewards dictionary.

        Typically called near the end of a step() method
        """
        for agent, reward in self.rewards.items():
            self._cumulative_rewards[agent] += reward



    """
    Dead Agent Handlers
    NOTE: Not used by our env since we respawn players
    """
    # def _deads_step_first(self) -> AgentID:
    #     """Makes .agent_selection point to first terminated agent.

    #     Stores old value of agent_selection so that _was_dead_step can restore the variable after the dead agent steps.
    #     """
    #     _deads_order = [
    #         agent
    #         for agent in self.agents
    #         if (self.terminations[agent] or self.truncations[agent])
    #     ]
    #     if _deads_order:
    #         self._skip_agent_selection = self.agent_selection
    #         self.agent_selection = _deads_order[0]
    #     return self.agent_selection

    # def _was_dead_step(self, action: None) -> None:
    #     """Helper function that performs step() for dead agents.

    #     Does the following:

    #     1. Removes dead agent from .agents, .terminations, .truncations, .rewards, ._cumulative_rewards, and .infos
    #     2. Loads next agent into .agent_selection: if another agent is dead, loads that one, otherwise load next live agent
    #     3. Clear the rewards dict

    #     Examples:
    #         Highly recommended to use at the beginning of step as follows:

    #     def step(self, action):
    #         if (self.terminations[self.agent_selection] or self.truncations[self.agent_selection]):
    #             self._was_dead_step()
    #             return
    #         # main contents of step
    #     """
    #     if action is not None:
    #         raise ValueError("when an agent is dead, the only valid action is None")

    #     # removes dead agent
    #     agent = self.agent_selection
    #     assert (
    #         self.terminations[agent] or self.truncations[agent]
    #     ), "an agent that was not dead as attempted to be removed"
    #     del self.terminations[agent]
    #     del self.truncations[agent]
    #     del self.rewards[agent]
    #     del self._cumulative_rewards[agent]
    #     del self.infos[agent]
    #     self.agents.remove(agent)

    #     # finds next dead agent or loads next live agent (Stored in _skip_agent_selection)
    #     _deads_order = [
    #         agent
    #         for agent in self.agents
    #         if (self.terminations[agent] or self.truncations[agent])
    #     ]
    #     if _deads_order:
    #         if getattr(self, "_skip_agent_selection", None) is None:
    #             self._skip_agent_selection = self.agent_selection
    #         self.agent_selection = _deads_order[0]
    #     else:
    #         if getattr(self, "_skip_agent_selection", None) is not None:
    #             assert self._skip_agent_selection is not None
    #             self.agent_selection = self._skip_agent_selection
    #         self._skip_agent_selection = None
    #     self._clear_rewards()

    # def __str__(self) -> str:
    #     """Returns a name which looks like: `space_invaders_v1`."""
    #     if hasattr(self, "metadata"):
    #         return self.metadata.get("name", self.__class__.__name__)
    #     else:
    #         return self.__class__.__name__