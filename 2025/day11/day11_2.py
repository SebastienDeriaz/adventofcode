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

    
    # nx.draw(g, node_size=5, with_labels=False)
    # plt.show()
    


    # dac -> fft : 0
    # fft -> dac : ?

    svr_fft = list(nx.all_simple_paths(g, 'fft', 'dac'))

    print(len(svr_fft))

    return

    #svr_dac = nx.all_simple_paths(g, 'svr', 'dac')

    #fft_dac = nx.all_simple_paths(g, 'fft', 'dac')

    #dac_fft = nx.all_simple_paths(g, 'dac', 'fft')


    # dac_fft = list(nx.all_simple_paths(g, 'dac', 'fft'))
    # print(len(dac_fft))


    fft_dac = list(nx.all_simple_edge_paths(g, 'fft', 'dac'))
    print(len(fft_dac))

    return
    fft_out = list(nx.all_simple_paths(g, 'fft', 'out'))

    print(len(fft_out))

    svr_dac = list(nx.all_simple_paths(g, 'svr', 'dac'))

    print(len(svr_dac))

    return


    

if __name__ == '__main__':
    main()