import sys
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from itertools import combinations, permutations

UP = np.array([1, 0])
DOWN = np.array([-1, 0])
RIGHT = np.array([0, 1])
LEFT = np.array([0, -1])

DIRECTIONS = [UP, DOWN, LEFT, RIGHT]

WALL = '#'
START = 'S'
END = 'E'
VISITED = 'x'
EMPTY = '.'

TURN_COST = 1000
FORWARD_COST = 1

def print_matrix(matrix):
    for line in matrix:
        print(''.join(line))

def parse_file(file):
    with open(file) as f:
        data = f.read()
        values = [list(line) for line in data.split('\n') if line]
        return np.array(values)


def node_name(p):
    return f'{p[0]}-{p[1]}'

def node_pos(name : str):
    r, c = [int(x) for x in name.split('-')]
    return (c, r)

def recurse_build_network(array : np.ndarray, network : nx.Graph, start : np.ndarray, direction : np.ndarray, cost : int = 1):
    p = start
    while True:
        network.add_node(node_name(p), start=array[tuple(p)] == START, end=array[tuple(p)] == END)

        n = node_name(p)

        new_positions = []
        for d in DIRECTIONS:
            if np.array_equal(-d, direction):
                continue
            p2 = p + d
            if array[tuple(p2)] in [EMPTY, END] and not network.has_edge(n, node_name(p2)):
                cost_delta = FORWARD_COST
                new_positions.append((d, cost_delta))
        
        #print(f'New positions : {new_positions}')
        if len(new_positions) == 0:
            # Stuck
            break
        elif len(new_positions) == 1:
            # Go to the position
            d, cost_delta = new_positions[0]
            p2 = p + d
            n2 = node_name(p2)
            if network.has_edge(n, n2):
                # Break the cycle
                break
            else:
                network.add_edge(n, n2, weight=cost_delta)
                p = p2
                direction = d
                cost += cost_delta
        else:
            # Recurse
            for d, cost_delta in new_positions:
                p2 = p + d
                n2 = node_name(p2)
                network.add_edge(n, n2, weight=cost_delta)
                recurse_build_network(array, network, p2, d, cost + cost_delta)


def make_network(array : np.ndarray):
    g = nx.Graph()

    start = np.array(np.where(array == START)).squeeze()

    end = np.array(np.where(array == END)).squeeze()

    recurse_build_network(array, g, start.copy(), RIGHT)

    return g, start, end


def update_network(network : nx.Graph):
    neighbors_per_node = [(n, list(nx.neighbors(network, n))) for n in network.nodes]
    neighbors_per_node.sort(key=lambda x : len(x[1]))
    
    for node, neighbors in neighbors_per_node:
        if network.nodes[node]['start']:
            # All of the edges that are not facing RIGHT are TURN
            for n in neighbors:
                v = tuple(np.array(node_pos(n)) - np.array(node_pos(node)))
                if v != (1, 0):
                    network[node][n]['weight'] = FORWARD_COST + TURN_COST
        elif network.nodes[node]['end']:
            pass
        elif len(neighbors) > 2:
            for a, b in permutations(neighbors, 2):
                offset = np.array(node_pos(a)) - np.array(node_pos(b))
                if offset[0] != 0 and offset[1] != 0:
                    cost = 2*FORWARD_COST + TURN_COST
                else:
                    cost = 2*FORWARD_COST
                network.add_edge(a, b, weight=cost)
        
            network.remove_node(node)
        elif len(neighbors) == 2:
            v1 = np.array(node_pos(node)) - np.array(node_pos(neighbors[0]))
            v2 = np.array(node_pos(node)) - np.array(node_pos(neighbors[1]))
            if np.dot(v1, v2) == 0:
                network[node][neighbors[0]]['weight'] = TURN_COST // 2 + FORWARD_COST
                network[node][neighbors[1]]['weight'] = TURN_COST // 2 + FORWARD_COST

            #     network.add_edge(*neighbors, weight = 2*FORWARD_COST + TURN_COST)
            #     network.remove_node(node)
        


        


def main():
    array = parse_file(sys.argv[1])

    network, start, end = make_network(array)

    update_network(network)

    path = nx.dijkstra_path(network, node_name(start), node_name(end))

    cost = 0
    for n1, n2 in zip(path[:-1], path[1:]):
        cost += network.get_edge_data(n1, n2)['weight']

    print(cost)

    return
    plt.figure(figsize=(40,40))
    pos = {node : node_pos(node) for node in network.nodes}
    nodes = set(network.nodes)
    path_nodes = set(path)
    nx.draw_networkx_nodes(network, pos, nodelist = nodes - path_nodes, node_size=20)
    nx.draw_networkx_nodes(network, pos, nodelist = path_nodes, node_color='red', node_size=20)
    nx.draw_networkx_edges(network, pos, label=True)
    labels = nx.get_edge_attributes(network, 'weight')
    nx.draw_networkx_edge_labels(network, pos, edge_labels=labels)

    plt.gca().invert_yaxis()

    plt.show()

if __name__ == '__main__':
    main()