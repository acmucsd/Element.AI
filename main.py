import asyncio
from typing import Dict, List
import numpy as np
import json
import sys
import random
# from omegaconf import OmegaConf

from luxai_runner.bot import Bot
from luxai_runner.episode import Episode, EpisodeConfig, ReplayConfig
# from luxai_runner.tournament import Tournament
from luxai_runner.logger import Logger

from paperio import PaperIO

def main():
    import argparse

    parser = argparse.ArgumentParser(description="Run the Element AI game.")
    parser.add_argument("players", nargs="+", help="Paths to player modules. If --tournament is passed as well, you can also pass a folder and we will look through all sub-folders for valid agents with main.py files (only works for python agents at the moment).")
    parser.add_argument("-l", "--len", help="Max episode length", type=int, default=300)

    # replay configs
    parser.add_argument("-o", "--output", help="Where to output replays. Default is none and no replay is generated")
    parser.add_argument("--replay.save_format", help="Save format \"json\" works with the visualizer while pickle is a compact, python usable version", default="json")

    # episode configs
    parser.add_argument(
        "-v", "--verbose", help="Verbose Level (0 = silent, 1 = errors, 2 = warnings, 3 = info)", type=int, default=1
    )

    # env configs
    parser.add_argument("-s", "--seed", help="Fix a seed for episode(s). All episodes will initialize the same.", type=int)
    parser.add_argument("--render", help="Render with a window", action="store_true", default=False)


    args = parser.parse_args()

    num_players = len(args.players)
    map_size = 70 if num_players == 2 else 85 if num_players == 3 else 100 if num_players == 4 else 70

    # TODO make a tournament runner ranked by ELO, Wins/Losses, Trueskill, Bradley-Terry system
    cfg = EpisodeConfig(
            players=args.players,
            num_players = len(args.players),
            env_cls=PaperIO,
            seed=args.seed,
            env_cfg=dict(
                num_players=len(args.players),
                max_episode_length=args.len,
                map_size=map_size,
            ),
            verbosity=args.verbose,
            save_replay_path=args.output,
            replay_options=ReplayConfig(
                save_format=getattr(args, "replay.save_format"),
                # compressed_obs=getattr(args, "replay.compressed_obs")
            ),
            render=args.render,
        )

    import time
    stime = time.time()
    eps = Episode(
        cfg=cfg
    )
    rewards = asyncio.run(eps.run())
    etime = time.time()
    import json
    out = json.dumps(rewards)
    print(out)
if __name__ == "__main__":
    main()