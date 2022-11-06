import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--env', help='Environment to run. Either Angular or Grid', default='Angular')

def get_args():
    return parser.parse_args()