from dataclasses import dataclass, field
from typing import Dict
import numpy as np
def process_action(action):
    return to_json(action)
def to_json(obj):
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, list) or isinstance(obj, tuple):
        return [to_json(s) for s in obj]
    elif isinstance(obj, dict):
        out = {}
        for k in obj:
            out[k] = to_json(obj[k])
        return out
    else:
        return obj
def from_json(state):
    if isinstance(state, list):
        return np.array(state)
    elif isinstance(state, dict):
        out = {}
        for k in state:
            out[k] = from_json(state[k])
        return out
    else:
        return state 

def process_obs(player, game_state, step, obs):
    return from_json(obs)
    # if step == 0:
    #     # at step 0 we get the entire map information
    #     game_state = from_json(obs)
    # else:
    #     # use delta changes to board to update game state
    #     obs = from_json(obs)
    #     for k in obs:
    #         if k != 'board':
    #             game_state[k] = obs[k]
    #         else:
    #             if "valid_spawns_mask" in obs[k]:
    #                 game_state["board"]["valid_spawns_mask"] = obs[k]["valid_spawns_mask"]
    #     for item in ["rubble", "lichen", "lichen_strains"]:
    #         for k, v in obs["board"][item].items():
    #             k = k.split(",")
    #             x, y = int(k[0]), int(k[1])
    #             game_state["board"][item][x, y] = v
    # return game_state
