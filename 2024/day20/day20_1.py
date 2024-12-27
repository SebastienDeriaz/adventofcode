import sys
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from tqdm import tqdm

WALL = '#'
THIN_WALL = '&'
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

def set_thin_walls(matrix):
    for r in range(1, matrix.shape[0]-1):
        for c in range(1, matrix.shape[1]-1):
            for d in [LEFT, DOWN]:
                p = np.array([r, c])
                p1 = p + d
                p2 = p - d
                if matrix[tuple(p)] in [WALL, START, END] and matrix[tuple(p1)] in [EMPTY, START, END] and matrix[tuple(p2)] in [EMPTY, START, END]:
                    matrix[tuple(p)] = THIN_WALL

def node_name(p):
    return f'{p[0]}-{p[1]}'

def node_pos(name : str):
    r, c = [int(x) for x in name.split('-')]
    return (c, r)


def matrix_to_network(matrix):
    network = nx.Graph()
    for r in range(matrix.shape[0]):
        for c in range(matrix.shape[1]):
            network.add_node(node_name(np.array([r, c])))

    for r in range(matrix.shape[0]):
        for c in range(matrix.shape[1]):
            p = np.array([r, c])
            for d in DIRECTIONS:
                p2 = p + d
                if matrix[tuple(p)] in [EMPTY, START, END] and matrix[tuple(p2)] in [EMPTY, START, END]:
                    n = node_name(p)
                    n2 = node_name(p2)
                    if not network.has_edge(n, n2):
                        network.add_edge(n, n2)

    return network

def find_shorter_paths(network : nx.Graph, matrix : np.ndarray):
    start = np.array(np.where(matrix == START)).squeeze()
    end = np.array(np.where(matrix == END)).squeeze()

    long_path = nx.astar_path(network, node_name(start), node_name(end))
    reference_path_length = len(long_path)-1


    paths_per_save = {}
    for r, c in tqdm(zip(*np.where(matrix == THIN_WALL))):
        new_network = network.copy()
        p = np.array([r, c])
        n = node_name(p)
        # Add the point
        for d in DIRECTIONS:
            p2 = p + d
            if matrix[tuple(p2)] in [EMPTY, START, END]:
                n2 = node_name(p2)
                new_network.add_edge(n, n2)

        path = nx.astar_path(new_network, node_name(start), node_name(end))
        saved = reference_path_length - (len(path)-1)
        if saved > 0:
            if saved not in paths_per_save:
                paths_per_save[saved] = 0
            paths_per_save[saved] += 1

    return paths_per_save


def main():
    matrix = parse_file(sys.argv[1])

    set_thin_walls(matrix)

    network = matrix_to_network(matrix)

    paths_per_save = find_shorter_paths(network, matrix)

    paths_per_save = list(paths_per_save.items())
    paths_per_save.sort(key=lambda x : x[0])

    minimum = 100
    total = 0

    for saved, cheats in paths_per_save:
        if saved >= minimum:
            total += cheats
        #print(f'{cheats:2} that save {saved:2} picoseconds')
    
    print(total)

    return
    

    plt.figure(figsize=(20,20))
    pos = {node : node_pos(node) for node in network.nodes}
    nx.draw_networkx(network, pos)
    plt.gca().invert_yaxis()
    plt.show()



if __name__ == '__main__':
    main()