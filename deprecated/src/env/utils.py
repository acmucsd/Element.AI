import arcade
from .gridv1.game import GridEnvV1
from .gridv2.game import GridEnvV2
from .angular.game import AngularEnv
from .gridv1 import constants as GRID_CONSTANTS
from .gridv2 import constants as GRIDV2_CONSTANTS
from .angular import constants as ANGULAR_CONSTANTS

def create_env(env):
    if env.lower() == "gridv1":
        return GridEnvV1(GRID_CONSTANTS.SCREEN_WIDTH, GRID_CONSTANTS.SCREEN_HEIGHT, GRID_CONSTANTS.SCREEN_TITLE)
    elif env.lower() == "gridv2":
        return GridEnvV2(render=True)
    elif env.lower() == "angular":
        return AngularEnv(ANGULAR_CONSTANTS.SCREEN_WIDTH, ANGULAR_CONSTANTS.SCREEN_HEIGHT, ANGULAR_CONSTANTS.SCREEN_TITLE)
    else:
        raise ValueError("Invalid env name")

def step(env):
    while True:
        for i in range(10):
            env.step(direction=1)
        env.step(direction=-1)

def run_env(env):
    if type(env) == GridEnvV2:
        step(env)
    else:
        env.setup()
        arcade.run()