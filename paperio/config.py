from argparse import Namespace
from dataclasses import dataclass
from typing import Dict, List

@dataclass
class EnvConfig:
    """
    Max Vals
    """
    max_players: int = 4
    max_episode_length: int = 300

    """
    Set During Configuration
    """
    map_size: int = 100
    num_players: int = 1


    """
    Board Configs
    """
    bomb_count: int = 10
    bomb_respawn_rate: int = 0

    boost_count: int = 40
    boost_respawn_rate: int = 0

