import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--env', help='Environment to run. Either angular or grid', default='angular')

def get_args():
    return parser.parse_args()