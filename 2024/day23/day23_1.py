import sys
import networkx as nx


def parse_data(data):
    G = nx.Graph()
    for line in data.split('\n'):
        a, b = line.split('-')
        G.add_node(a)
        G.add_node(b)
        G.add_edge(a, b)

    return G

def main():
    file = sys.argv[1]
    with open(file) as f:
        network = parse_data(f.read())

        groups = []

        for node in network.nodes:
            if node.startswith('t'):
                # Consider this one
                for n in network.neighbors(node):
                    for n2 in network.neighbors(n):
                        if network.has_edge(n2, node):
                            # There is a group of 3
                            triangle = [node, n, n2]
                            triangle.sort()
                            if tuple(triangle) not in groups:
                                groups.append(tuple(triangle))

        print(len(groups))

if __name__ == '__main__':
    main()