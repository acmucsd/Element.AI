from argparse import Namespace
from dataclasses import dataclass
import dataclasses
from typing import Dict, List

class EnvConfig:
    """
    Max Vals
    """
    max_players: int = 4
    max_episode_length: int = 1000

    """
    Set During Configuration
    """
    map_size: int = 100
    num_players: int = 1


    """
    Board Configs
    """
    bomb_count: int = 10
    boost_count: int = 40