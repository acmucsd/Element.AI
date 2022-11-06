import arcade
from env.utils import *

ENV = "Angular"


def main():
    env = create_env(ENV)
    env.setup()
    arcade.run()


if __name__ == "__main__":
    main()