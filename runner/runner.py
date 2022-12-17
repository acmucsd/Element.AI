import argparse
from env.game import GridEnvV2, EnvConfig
from agent.agent import Agent
import json

def main():

    # General Args
    parser = argparse.ArgumentParser(description="Run the ACM AI SP22 Paper IO Grid environment.")
    parser.add_argument("players", nargs="+", help="Paths to player modules. Must be listed individually.")

    # Env Args
    parser.add_argument("-l", "--len", help="Max episode length", type=int, default=1000)
    parser.add_argument("-r", "--rows", help="Number of rows", type=int, default=100)
    parser.add_argument("-c", "--cols", help="Number of columns", type=int, default=100)

    
    args = parser.parse_args()

    cfg = EnvConfig(
        players=args.players,
        rows=args.rows,
        cols=args.cols,
        max_iterations=args.len
    )

    """
    Init Phase
    """
    env = GridEnvV2(cfg=cfg)



    """
    Game Phase
    """

    def read_input():
        """
        Reads input from stdin
        """
        try:
            return input()
        except EOFError as eof:
            raise SystemExit(eof)
    
    env.iteration = 0
    player_agents = {}
    while (env.iteration < env.cfg.max_iterations):

        for player_id in env.cfg.players:

            if (env.iteration == 0):
                player_agents[player_id] = Agent(player_id)

            agent = player_agents[player_id]
            
            game_data = env.get_game_data(player_id)
            game_data_json = json.loads(game_data)

            # print(game_data)

            direction = agent.act(game_data_json["player_info"], game_data_json["game_info"])

            env.step(player_id, direction)

        env.iteration += 1

    return

if __name__ == "__main__":
    main()