from sys import argv
from enum import Enum
import re
from math import lcm

LEFT = 'L'
RIGHT = 'R'

def is_start_node(x : str):
    return x.endswith('A')

def is_end_node(x : str):
    return x.endswith('Z')


def parse_key_nodes(data):
    nodes = {}
    node_pattern = '(\w+) = \((\w+), (\w+)\)'
    for i, line in enumerate(data.split('\n')):
        if i == 0:
            # Parse the first line
            key = list(line)
        elif line != '':
            node, left, right = re.match(node_pattern, line).groups()
            nodes[node] = (left, right)

    return key, nodes

def end_iterations(key, nodes, max_iter=10e6):
    start_nodes = list(filter(is_start_node, nodes))
    end_nodes = list(filter(is_end_node, nodes))
    # Get the number of iterations for each start node
    iter_count= 0
    stop = False
    currents = start_nodes
    z_iterations = [[] for _ in start_nodes]
    while iter_count < max_iter and not stop:
        for direction in key:
            d = 0 if direction == LEFT else 1
            currents = [nodes[c][d] for c in currents]
            iter_count += 1

            all_multiple_of_previous = True
            for i, c in enumerate(currents):
                if is_end_node(c):
                    if any([(iter_count % x == 0) for x in z_iterations[i]]):
                        # This iter_count is a multiple of a previous one
                        pass
                    else:
                        all_multiple_of_previous = False
                        z_iterations[i].append(iter_count)
            if all_multiple_of_previous and all([len(x) > 0 for x in z_iterations]):
                stop = True
                break

                
             
            # if all([is_end_node(x) for x in currents]):
            #     stop = True
            #     break
    iterations = lcm(*[x[0] for x in z_iterations])
    return iterations
    




def main():
    file = argv[1]
    with open(file) as f:
        data = f.read()
        key, nodes = parse_key_nodes(data)
        print(end_iterations(key, nodes))


if __name__ == '__main__':
    main()