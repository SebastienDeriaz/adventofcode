from sys import argv
from enum import Enum
import re

LEFT = 'L'
RIGHT = 'R'


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
            


def find_node(key, nodes, destination, max_iter=1e6):
    current = list(nodes.keys())[0]
    iter_count= 0
    stop = False
    while iter_count < max_iter and not stop:
        for direction in key:
            if direction == LEFT:
                current = nodes[current][0]
            else:
                current = nodes[current][1]
            iter_count += 1
            if current == destination:
                stop = True
                break
    if stop:
        return iter_count
    else:
        return None




def main():
    file = argv[1]
    with open(file) as f:
        data = f.read()
        key, nodes = parse_key_nodes(data)
        print(find_node(key, nodes, 'ZZZ'))


if __name__ == '__main__':
    main()