from env.utils import *
from arguments import get_args


def main(args):
    env = create_env(args.env)
    run_env(env)


if __name__ == "__main__":
    args = get_args()
    main(args)