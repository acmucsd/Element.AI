#Load the data from the json
import json
import numpy as np
from constants import *
import cv2

def main():

    import argparse

    parser = argparse.ArgumentParser(description="Generate a replay script from a replay json file.")
    parser.add_argument("file", nargs=1, help="The replay json file to convert to video. Only one replay file at a time.")
    parser.add_argument("-o", "--out", help="Out file name (defaults to output_vid)", type=str, default='output_vid')

    args = parser.parse_args()

    print('Opening File...')
    f = open(args.file[0])
    print('File Opened!')

    print('Loading JSON Data...')
    data = json.load(f)
    print('JSON Data Loaded!')


    print('Processing Data and Converting to Video...')
    first_obs = np.array(data['observations'][0]['board']['board_state'])
    map_size = first_obs.shape[0]

    scale_factor = 10
    frameSize = (map_size * scale_factor, map_size * scale_factor)

    out = cv2.VideoWriter(f'{args.out}.mp4',cv2.VideoWriter_fourcc(*'mp4v'), 1, frameSize)

    i = 1
    for obs in data['observations']:

        grid = np.array(obs['board']['board_state'])
        player_num_grid = np.array(obs['board']['players_state'])
        num_agents = len(obs.keys()) - 1

        heads = []
        for key in obs.keys():
            if key != 'board':
                heads.append(obs[key]['head'])

        Numpy_rgb = obs_to_rgb(grid, player_num_grid, heads, num_agents=num_agents)
        Numpy_rgb = np.repeat(a=np.repeat(a=Numpy_rgb, repeats=scale_factor,axis=0), repeats=scale_factor, axis=1)
        out.write(Numpy_rgb) # write them to video output

        progress_bar(i, len(data['observations']))

        i += 1

    out.release() # release the video output

    print('Video Generated!')


def obs_to_rgb(grid, player_num_grid, heads, num_agents=0):

    map_size = grid.shape[0]
    rgb_array = np.zeros((map_size, map_size, 3), dtype=np.uint8)

    for i in range(num_agents):
        rgb_array[np.logical_and(grid == PASSED, player_num_grid == i)] = PLAYER_COLORS[i][0]
        rgb_array[np.logical_and(grid == OCCUPIED, player_num_grid == i)] = PLAYER_COLORS[i][1]
    for head in heads:
        x,y = head
        rgb_array[y,x] = PLAYER_HEAD_COLOR
    rgb_array[grid == UNOCCUPIED] = WHITE_SMOKE
    rgb_array[grid == BOMB] = BLACK
    rgb_array[grid == BOOST] = PURPLE

    return rgb_array

def progress_bar(current, total, bar_length=20):
    fraction = current / total

    arrow = int(fraction * bar_length - 1) * '-' + '>'
    padding = int(bar_length - len(arrow)) * ' '

    ending = '\n' if current == total else '\r'

    print(f'Progress: [{arrow}{padding}] {int(fraction*100)}%', end=ending)


if __name__ == '__main__':
    main()