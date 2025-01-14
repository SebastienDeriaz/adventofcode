import sys
import networkx as nx
import matplotlib.pyplot as plt

def parse_data(data):
    G = nx.Graph()
    for line in data.split('\n'):
        a, b = line.split('-')
        G.add_node(a)
        G.add_node(b)
        G.add_edge(a, b)

    return G

def find_clusters(network : nx.Graph):
    clusters = []
    for node in network.nodes():
        # Create a cluster
        cluster = set(network.neighbors(node)) | set([node])
        while True:
            for n in cluster:
                if n == node:
                    continue
                n2 = set(network.neighbors(n))
                if cluster not in n2:
                    missing = cluster - n2 - set([n]) - set([node])
                    if len(missing) > 0:
                        # This cluster is not valid anymore, reduce it
                        cluster -= missing
                        break
            else:
                break
        if cluster not in clusters and len(cluster) > 1:
            clusters.append(cluster)

    return clusters

def main():
    file = sys.argv[1]
    with open(file) as f:
        network = parse_data(f.read())

        clusters = find_clusters(network)

        clusters.sort(key=lambda cluster : len(cluster))

        biggest_cluster = list(clusters[-1])
        biggest_cluster.sort()
        
        print(','.join(biggest_cluster))            

if __name__ == '__main__':
    main()