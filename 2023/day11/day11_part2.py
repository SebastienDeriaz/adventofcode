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



def find_expand_axes(matrix : np.ndarray):
    axes = []
    for axis in [0, 1]:
        empty_mask = np.sum(matrix, axis=axis) == 0
        axes += [(axis, n) for n in np.where(empty_mask)[0]]
    return axes

def distance_between(p1, p2, expand_axes, N):
    # It is simple the mahnatan distance
    distance = abs(p2[1] - p1[1]) + abs(p2[0] - p1[0])
    for a, n in expand_axes:
        if p1[a] <= n <= p2[a] or p2[a] <= n <= p1[a]:
            distance += N
    return distance
        


def calculate_distances(matrix, expand_axes, N):
    galaxies = {}
    yx = np.where(matrix > 0)
    i = 1
    for y, x in zip(*yx):
        galaxies[i] = (x, y)
        i += 1
    
    distances = {}
     
    for ai, pa in galaxies.items():
        for bi, pb in list(galaxies.items())[ai:]:
            distances[(ai, bi)] = distance_between(pa, pb, expand_axes, N)

    return distances

def main():
    file = argv[1]
    with open(file) as f:
        data = f.read()
        matrix = parse_universe(data)
        expand_axes = find_expand_axes(matrix)
        print(expand_axes)
        N = 1_000_000-1
        distances = calculate_distances(matrix, expand_axes, N)
        print(sum(distances.values()))

if __name__ == '__main__':
    main()
