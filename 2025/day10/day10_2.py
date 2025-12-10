import itertools
from sys import argv
import numpy as np
from scipy.optimize import linprog
import networkx as nx

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
                    assert len(joltages) == N

            machines.append((N, lamps, buttons, joltages))


    for N, _, buttons, joltages in machines[1:]:

        print(f'Joltages : {joltages}')

        #buttons = [(3,), (1,3), (2,3), (0,2), (0,1)]




        # def counters_to_node(counters : list):
        #     return '-'.join(str(c) for c in counters)
        
        # g = nx.graph.Graph()
        # for i, path in enumerate(itertools.product(enumerate(buttons), repeat=sum(joltages))):
        #     counters = [0]*N

        #     cs = counters_to_node(counters)
        #     if not g.has_node(cs):
        #         g.add_node(cs)

        #     start_node = cs
        #     for bi, b in path:
        #         for ci in b:
        #             counters[ci] += 1
                
        #         end_node = counters_to_node(counters)
        #         if not g.has_node(cs):
        #             g.add_node(cs)

        #         g.add_edge(start_node, end_node, button_id=bi)


        #     #print(path)


        # #print(nx.shortest_path(g, counters_to_node([0]*N), counters_to_node(joltages)))

        # print(g.nodes)

        M = np.zeros((N, len(buttons)))

        for bi, button in enumerate(buttons):
            M[button, bi] = 1
        print(M)

        Mp = np.linalg.pinv(M)

        #b_eq = np.array([2, 1, 1])
        #c = np.zeros(len(buttons))
        #bounds = [(0, max(joltages))] * len(buttons)

        # res = linprog(c, A_eq=M, b_eq=joltages, bounds=bounds, method='highs-ipm')
        # if res.success:
        #     print(f'Presses : {res.x} ({sum(res.x)})')

        #     print(M @ res.x)

        #print(np.array([1, 3, 0, 3, 1, 2]).round(1))
        print(Mp @ joltages)
        print(f'Presses : {np.sum((Mp @ joltages))}')

        #print(M @ np.array([1, 3, 0, 3, 1, 2]))
        
        # 1      3      0      3      1      2
        # 1+7/11 3+1/11 0+7/11 2+3/11 1+1/11 1+10/11

        # 7 -> floor
        # 1 -> floor
        # 7 -> floor
        # 3 -> ceil
        # 1 -> floor
        # 10 -> ceil

        2 
        3 4 -1




        break


        #break

if __name__ == '__main__':
    main()