import sys
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt


VALID = '.'
CORRUPTED = '#'
VISITED = 'O'

UP = np.array([-1, 0])
DOWN = np.array([1, 0])
LEFT = np.array([0, -1])
RIGHT = np.array([0, 1])

DIRECTIONS = [UP, DOWN, LEFT, RIGHT]

def parse_file(file):
    coordinates = []
    with open(file) as f:
        for line in f.read().split('\n'):
            if line:
                x, y = [int(x) for x in line.split(',')]
                coordinates.append((y, x))

    return coordinates

def node_name(p : np.ndarray):
    return f'{p[0]}-{p[1]}'

def make_network(N : int, coordinates : list, n_fall : int):
    used_coordinates = coordinates[:n_fall]
    network = nx.Graph()
    # 1) Generate all nodes
    for r in range(N):
        for c in range(N):
            p = np.array([r, c])
            network.add_node(node_name(p), valid=tuple(p) not in used_coordinates)

    # 2) Add links
    for r in range(N):
        for c in range(N):
            p = np.array([r, c])
            n = node_name(p)
            if network.nodes[n]['valid']:
                for d in DIRECTIONS:
                    p2 = p + d
                    n2 = node_name(p2)
                    if 0 <= p2[0] < N and 0 <= p2[1] < N:
                        if network.nodes[n2]['valid']:
                            # Connect to it
                            network.add_edge(n, n2)

    return network

def node_pos(name : str):
    r, c = [int(x) for x in name.split('-')]
    return (c, r)

def main():
    file, N, n_fall = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])


    start = np.array([0,0])
    end = np.array([N-1, N-1])
    coordinates = parse_file(file)

    network = make_network(N, coordinates, n_fall)

    path = nx.astar_path(network, node_name(start), node_name(end))
    print(len(path)-1)

if __name__ == '__main__':
    main()
