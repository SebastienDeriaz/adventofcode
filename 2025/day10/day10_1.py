import networkx as nx
import matplotlib.pyplot as plt
from networkx.exception import NetworkXNoPath
from sys import argv

def main():

    file = argv[1]
    machines = []
    with open(file) as f:
        file_contents = f.read()

        for line in file_contents.split('\n'):
            buttons = []
            for fragment in line.split(' '):
                if fragment.startswith('['):
                    lamp_string = fragment[1:-1]

                    lamps = sum([2**i * (1 if x=='#' else 0) for i, x in zip(range(0, len(lamp_string)), lamp_string)])
                    N = len(lamp_string)

                elif fragment.startswith('('):
                    buttons.append([int(x) for x in fragment[1:-1].split(',')])

                elif fragment.startswith('{'):
                    joltages = [int(x) for x in fragment[1:-1].split(',')]

            machines.append((N, lamps, buttons, joltages))

    total_button_presses = 0
    for mi, (N, lamp, buttons, _) in enumerate(machines):
        g = nx.graph.Graph()
        
        [g.add_node(x) for x in range(2**N)]

        for bi, button in enumerate(buttons):
            mask = sum([2**k for k in button])
            #print(f'Button {bi} : {button} ({mask})')
            added_edges = []
            for start in range(2**N):
                end = start ^ mask

                #print(f'{start} -> {end}')

                if not g.has_edge(start, end):
                    added_edges.append((start, end))
                    g.add_edge(start, end, button_id=bi)




        try:
            sp = nx.shortest_path(g, 0, lamp)
            #raise NetworkXNoPath()
        except NetworkXNoPath:
            print(f'No path for machine {mi}')
            nx.draw(g, with_labels=True)
            plt.show()
        else:
            buttons_to_press = []
            for s, e in zip(sp[:-1], sp[1:]):
                buttons_to_press.append(g.get_edge_data(s, e)['button_id'])

            print(f'Machine {mi} : {len(buttons_to_press)} presses')

            total_button_presses += len(buttons_to_press) 

    #plt.show()

    print(total_button_presses)

if __name__ == '__main__':
    main()