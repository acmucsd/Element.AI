import json
from typing import Dict
from argparse import Namespace
import sys
from agent import Agent
from tools.tools import process_obs, to_json, from_json, process_action
### DO NOT REMOVE THE FOLLOWING CODE ###
agent_dict = dict() # store potentially multiple dictionaries as kaggle imports code directly
agent_prev_obs = dict()
def agent_fn(observation):
    """
    agent definition for kaggle submission.
    """
    global agent_dict
    step = observation.step
    curr_step = observation.curr_step
    
    
    player = observation.player
    remainingOverageTime = observation.remainingOverageTime
    if step == 0:
        agent_dict[player] = Agent(player)
        agent_prev_obs[player] = dict()
        agent = agent_dict[player]
    agent = agent_dict[player]
    obs = process_obs(player, agent_prev_obs[player], step, json.loads(observation.obs))
    agent_prev_obs[player] = obs
    agent.step = step
    
    actions = agent.act(step, curr_step, obs, remainingOverageTime)

    return process_action(actions)

if __name__ == "__main__":
    
    def read_input():
        """
        Reads input from stdin
        """
        try:
            return input()
        except EOFError as eof:
            raise SystemExit(eof)
    step = 0
    player_id = 0
    configurations = None
    i = 0
    while True:
        inputs = read_input()
        obs = json.loads(inputs)
        
        observation = Namespace(**dict(step=obs["step"], curr_step=obs['curr_step'], obs=json.dumps(obs["obs"]), remainingOverageTime=obs["remainingOverageTime"], player=obs["player"], info=obs["info"]))
        i += 1
        actions = agent_fn(observation)

        if (type(actions) != dict):
            actions = {}

        # send actions to engine
        print(json.dumps(actions))