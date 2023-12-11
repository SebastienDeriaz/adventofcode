from sys import argv
import numpy as np
from enum import Enum

EMPTY = 0
GALAXY = 1

TYPE_MAP = {
    '#' : GALAXY,
    '.' : EMPTY
}

def parse_universe(data):
    values = []
    for line in data.split('\n'):
        if line != '':
            values.append([TYPE_MAP[x] for x in line])
    return np.array(values)


def expand_universe(matrix : np.ndarray):
    for axis in [0, 1]:
        n_counter = 0
        empty_mask = np.sum(matrix, axis=axis) == 0
        for n in np.where(empty_mask)[0]:
            n += n_counter
            n_counter += 1
            if axis == 0:
                matrix = np.concatenate([matrix[:, :n+1], matrix[:, n:]], axis=1)
            else:
                matrix = np.concatenate([matrix[:n+1, :], matrix[n:, :]], axis=0)
    return matrix

            


def distance_between(p1, p2):
    # It is simple the mahnatan distance
    return abs(p2[1] - p1[1]) + abs(p2[0] - p1[0])
        


def calculate_distances(matrix):
    
    galaxies = {}
    yx = np.where(matrix > 0)
    i = 1
    for y, x in zip(*yx):
        galaxies[i] = (x, y)
        i += 1
    
    distances = {}
     
    for ai, pa in galaxies.items():
        for bi, pb in list(galaxies.items())[ai:]:
            distances[(ai, bi)] = distance_between(pa, pb)

    return distances

def main():
    file = argv[1]
    with open(file) as f:
        data = f.read()
        matrix = parse_universe(data)
        matrix = expand_universe(matrix)
        distances = calculate_distances(matrix)
        print(sum(distances.values()))

if __name__ == '__main__':
    main()
