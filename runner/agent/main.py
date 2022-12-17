import json
from typing import Dict
from argparse import Namespace

import uuid
from env.game import GridEnvV2
from agent import Agent

### DO NOT REMOVE THE FOLLOWING CODE ###
agent_dict = dict() # store potentially multiple dictionaries as kaggle imports code directly
agent_prev_obs = dict()
def agent_fn(step: int):
    global agent_dict
    
    player = 0
    if step == 0:
        agent_dict[player] = Agent(player)
        agent_prev_obs[player] = dict()
    agent = agent_dict[player]
    agent.step = step
    if (step == 0):
        direction = agent.early_setup()
    else:
        direction = agent.act()

    return direction

def main():

    def read_input():
        """
        Reads input from stdin
        """
        try:
            return input()
        except EOFError as eof:
            raise SystemExit(eof)

    

    while (iteration < 1):
        
        # NOTE: these sections will be separated when we create the runner
        # engine section
        

        # agent section
        direction = agent_fn(iteration)
        # env.step(player_id, direction, iteration)
        iteration += 1

if __name__ == "__main__":
    main()