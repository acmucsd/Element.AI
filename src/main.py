import arcade
from env.utils import *

ENV = "Angular" # can either be "Grid" or "Angular"


def main():
    env = create_env(ENV)
    env.setup()
    arcade.run()


if __name__ == "__main__":
    main()