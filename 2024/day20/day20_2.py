import sys
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from tqdm import tqdm
import json

WALL = '#'
EMPTY = '.'

START = 'S'
END = 'E'

UP = np.array([-1, 0])
DOWN = np.array([1, 0])
RIGHT = np.array([0, 1])
LEFT = np.array([0, -1])

DIRECTIONS = [UP, DOWN, RIGHT, LEFT]

def print_matrix(matrix):
    for row in matrix:
        print(''.join(row))

def parse_file(file):
    with open(file) as f:
        data = f.read()
        
        matrix = np.array([list(line) for line in data.split('\n') if line])

        return matrix

# def node_name(p):
#     return f'{p[0]}-{p[1]}'

# def node_pos(name : str):
#     r, c = [int(x) for x in name.split('-')]
#     return (c, r)


def matrix_to_network(matrix):
    network = nx.Graph()
    for r in range(matrix.shape[0]):
        for c in range(matrix.shape[1]):
            network.add_node((r, c))

    for r in range(matrix.shape[0]):
        for c in range(matrix.shape[1]):
            p = np.array([r, c])
            for d in DIRECTIONS:
                p2 = p + d
                if matrix[tuple(p)] in [EMPTY, START, END] and matrix[tuple(p2)] in [EMPTY, START, END]:
                    if not network.has_edge(tuple(p), tuple(p2)):
                        network.add_edge(tuple(p), tuple(p2))

    return network

def print_distance(distance_matrix : np.ndarray):
    _max = distance_matrix.max()
    size = int(np.ceil(np.log10(_max)))
    
    def rep(x):
        if x < 0:
            return ' ' * size
        else:
            return f'{x:{size}}'

    string = ''
    for row in distance_matrix:
        string += ' '.join([rep(x) for x in row]) + '\n'

    print(string)


def count_cheats(distance_matrix : np.ndarray, cheat_length : int):
    cheats = {}
    for p in zip(*np.where(distance_matrix >= 0)):
        start = distance_matrix[p]
        rmin = max(-p[0], - cheat_length)
        rmax = min(distance_matrix.shape[0]-1-p[0], cheat_length)
        cmin = max(-p[1], - cheat_length)
        cmax = min(distance_matrix.shape[1]-1-p[1], cheat_length)

        #print(f'{p} ({start})')
        #print(f'dr : {rmin} to {rmax}')
        #print(f'dc : {cmin} to {cmax}')
        for dr in range(rmin, rmax+1):
            for dc in range(cmin, cmax+1):
                manhattan_distance = abs(dr) + abs(dc)
                if (manhattan_distance > cheat_length) or (dr == 0 and dc == 0):
                    # Ignore
                    continue
                p2 = (p[0] + dr, p[1] + dc)
                value = distance_matrix[p2]
                #print(f' ({dr:+d},{dc:+d}) -> {p2}({value})')
                if value > 0:
                    # Not a wall
                    saved = value - (start + manhattan_distance)
                    if saved > 0:
                        #print(f'  saved : {saved}')
                        if saved not in cheats:
                            cheats[saved] = 0
                        cheats[saved] += 1

    return cheats

def main():
    matrix = parse_file(sys.argv[1])

    network = matrix_to_network(matrix)

    start = np.array(np.where(matrix == START)).squeeze()
    end = np.array(np.where(matrix == END)).squeeze()

    path = nx.astar_path(network, tuple(start), tuple(end))

    distance = np.ones_like(matrix, dtype=int) * (-1)

    for i, p in enumerate(path):
        distance[p] = i
    
    cheats = count_cheats(distance, 20)

    cheats_count = list(cheats.items())
    cheats_count.sort(key=lambda x : x[0], reverse=True)

    SAVE_THRESHOLD = 100

    total = sum([count for saved, count in cheats_count if saved >= SAVE_THRESHOLD])

    print(total)

if __name__ == '__main__':
    main()