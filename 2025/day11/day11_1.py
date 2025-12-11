from sys import argv
import networkx as nx
import matplotlib.pyplot as plt

def main():
    
    file = argv[1]

    g = nx.DiGraph()

    with open(file) as f:
        file_contents = f.read()

        for line in file_contents.split('\n'):
            machine, outputs = line.split(':')

            for output in outputs.split(' '):
                if not output:
                    continue

                g.add_edge(machine, output)

    source = 'you'
    destination = 'out'

    all_paths = list(nx.all_simple_paths(g, source, destination))

    print(len(all_paths))


    

if __name__ == '__main__':
    main()