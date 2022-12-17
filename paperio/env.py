from pettingzoo import AECEnv

import warnings
from typing import Any, Dict, Iterable, Iterator, List, Optional, Tuple, TypeVar

import gymnasium.spaces
import numpy as np
import random

from paperio.config import EnvConfig
from paperio.player import Player
from paperio.constants import *

ObsType = TypeVar("ObsType")
ActionType = TypeVar("ActionType")
AgentID = str

ObsDict = Dict[AgentID, ObsType]
ActionDict = Dict[AgentID, ActionType]

class ACMAI2022(AECEnv):
    """The AECEnv steps agents one at a time.

    If you are unsure if you have implemented a AECEnv correctly, try running
    the `api_test` documented in the Developer documentation on the website.
    """

    metadata: Dict[str, Any] = {"render.modes": ["human", "html", "rgb_array"], "name": "acmai_2022_paperio"}

    # All agents that may appear in the environment
    possible_agents: List[AgentID]
    agents: List[AgentID]  # Agents active at any given time

    observation_spaces: Dict[
        AgentID, gymnasium.spaces.Space
    ]  # Observation space for each agent
    # Action space for each agent
    action_spaces: Dict[AgentID, gymnasium.spaces.Space]

    # Whether each agent has just reached a terminal state
    terminations: Dict[AgentID, bool]
    truncations: Dict[AgentID, bool]
    rewards: Dict[AgentID, float]  # Reward from the last step for each agent
    # Cumulative rewards for each agent
    _cumulative_rewards: Dict[AgentID, float]
    infos: Dict[
        AgentID, Dict[str, Any]
    ]  # Additional information from the last step for each agent

    agent_selection: AgentID  # The agent currently being stepped

    """
    Init Functions
    """

    def __init__(self, env_cfg: EnvConfig):

        self.env_cfg = env_cfg

        self.possible_agents = ["player_" + str(r) for r in range(self.env_cfg.max_players)]
        self.agents = self.possible_agents
        self.max_episode_length = self.env_cfg.max_episode_length

        self.setup()

        pass

    def setup(self):
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
    Env Runtime Functions
    """

    def step(self, action: ActionType) -> None:
        """Accepts and executes the action of the current agent_selection in the environment.

        Automatically switches control to the next agent.
        """
        raise NotImplementedError

    def reset(
        self,
        seed: Optional[int] = None,
        return_info: bool = False,
        options: Optional[dict] = None,
    ) -> None:
        """Resets the environment to a starting state."""
        raise NotImplementedError

    def seed(self, seed: Optional[int] = None) -> None:
        """Reseeds the environment (making the resulting environment deterministic)."""
        raise NotImplementedError(
            "Calling seed externally is deprecated; call reset(seed=seed) instead"
        )

    # TODO: Remove `Optional` type below
    def observe(self, agent: str) -> Optional[ObsType]:
        """Returns the observation an agent currently can make.

        `last()` calls this function.
        """
        raise NotImplementedError

    def render(self):
        """Renders the environment as specified by self.render_mode.

        Render mode can be `human` to display a window.
        Other render modes in the default environments are `'rgb_array'`
        which returns a numpy array and is supported by all environments outside of classic,
        and `'ansi'` which returns the strings printed (specific to classic environments).
        """
        raise NotImplementedError

    def state(self) -> np.ndarray:
        """State returns a global view of the environment.

        It is appropriate for centralized training decentralized execution methods like QMIX
        """
        raise NotImplementedError(
            "state() method has not been implemented in the environment {}.".format(
                self.metadata.get("name", self.__class__.__name__)
            )
        )

    def close(self):
        """Closes any resources that should be released.

        Closes the rendering window, subprocesses, network connections,
        or any other resources that should be released.
        """
        pass

    def observation_space(self, agent: AgentID) -> gymnasium.spaces.Space:
        """Takes in agent and returns the observation space for that agent.

        MUST return the same value for the same agent name

        Default implementation is to return the observation_spaces dict
        """
        warnings.warn(
            "Your environment should override the observation_space function. Attempting to use the observation_spaces dict attribute."
        )
        return self.observation_spaces[agent]

    def action_space(self, agent: str) -> gymnasium.spaces.Space:
        """Takes in agent and returns the action space for that agent.

        MUST return the same value for the same agent name

        Default implementation is to return the action_spaces dict
        """
        warnings.warn(
            "Your environment should override the action_space function. Attempting to use the action_spaces dict attribute."
        )
        return self.action_spaces[agent]

    @property
    def num_agents(self) -> int:
        return len(self.agents)

    @property
    def max_num_agents(self) -> int:
        return len(self.possible_agents)

    def _deads_step_first(self) -> AgentID:
        """Makes .agent_selection point to first terminated agent.

        Stores old value of agent_selection so that _was_dead_step can restore the variable after the dead agent steps.
        """
        _deads_order = [
            agent
            for agent in self.agents
            if (self.terminations[agent] or self.truncations[agent])
        ]
        if _deads_order:
            self._skip_agent_selection = self.agent_selection
            self.agent_selection = _deads_order[0]
        return self.agent_selection

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

    def agent_iter(self, max_iter: int = 2**63) -> AECIterable:
        """Yields the current agent (self.agent_selection).

        Needs to be used in a loop where you step() each iteration.
        """
        return AECIterable(self, max_iter)

    def last(
        self, observe: bool = True
    ) -> Tuple[Optional[ObsType], float, bool, bool, Dict[str, Any]]:
        """Returns observation, cumulative reward, terminated, truncated, info for the current agent (specified by self.agent_selection)."""
        agent = self.agent_selection
        assert agent
        observation = self.observe(agent) if observe else None
        return (
            observation,
            self._cumulative_rewards[agent],
            self.terminations[agent],
            self.truncations[agent],
            self.infos[agent],
        )

    def _was_dead_step(self, action: None) -> None:
        """Helper function that performs step() for dead agents.

        Does the following:

        1. Removes dead agent from .agents, .terminations, .truncations, .rewards, ._cumulative_rewards, and .infos
        2. Loads next agent into .agent_selection: if another agent is dead, loads that one, otherwise load next live agent
        3. Clear the rewards dict

        Examples:
            Highly recommended to use at the beginning of step as follows:

        def step(self, action):
            if (self.terminations[self.agent_selection] or self.truncations[self.agent_selection]):
                self._was_dead_step()
                return
            # main contents of step
        """
        if action is not None:
            raise ValueError("when an agent is dead, the only valid action is None")

        # removes dead agent
        agent = self.agent_selection
        assert (
            self.terminations[agent] or self.truncations[agent]
        ), "an agent that was not dead as attempted to be removed"
        del self.terminations[agent]
        del self.truncations[agent]
        del self.rewards[agent]
        del self._cumulative_rewards[agent]
        del self.infos[agent]
        self.agents.remove(agent)

        # finds next dead agent or loads next live agent (Stored in _skip_agent_selection)
        _deads_order = [
            agent
            for agent in self.agents
            if (self.terminations[agent] or self.truncations[agent])
        ]
        if _deads_order:
            if getattr(self, "_skip_agent_selection", None) is None:
                self._skip_agent_selection = self.agent_selection
            self.agent_selection = _deads_order[0]
        else:
            if getattr(self, "_skip_agent_selection", None) is not None:
                assert self._skip_agent_selection is not None
                self.agent_selection = self._skip_agent_selection
            self._skip_agent_selection = None
        self._clear_rewards()

    def __str__(self) -> str:
        """Returns a name which looks like: `space_invaders_v1`."""
        if hasattr(self, "metadata"):
            return self.metadata.get("name", self.__class__.__name__)
        else:
            return self.__class__.__name__

    @property
    def unwrapped(self) -> AECEnv:
        return self