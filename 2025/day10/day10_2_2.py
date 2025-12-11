import itertools
from sys import argv
import numpy as np
from scipy.optimize import linprog
import networkx as nx
from itertools import combinations_with_replacement
from functools import lru_cache
from itertools import combinations

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
                    buttons.append(tuple([int(x) for x in fragment[1:-1].split(',')]))

                elif fragment.startswith('{'):
                    joltages = [int(x) for x in fragment[1:-1].split(',')]
                    assert len(joltages) == N

            machines.append((N, lamps, tuple(buttons), joltages))


    total_presses = 0
    for N, _, buttons, joltages in machines:

        print(f'Joltages : {joltages}')
        print(f'Buttons : {buttons}')


        M = np.zeros([len(joltages), len(buttons)])

        for bi, button in enumerate(buttons):
            M[button, bi] = 1

        # M = np.block([
        #     [0, 0, 0, 0, 1, 1],
        #     [0, 1, 0, 0, 0, 1],
        #     [0, 0, 1, 1, 1, 0],
        #     [1, 1, 0, 1, 0, 0],
        # ])

        # best = None
        # for x in combinations(M.T, len(joltages)):
        #     M2 = np.stack(x, axis=1)

        #     try:
        #         p = np.linalg.pinv(M2) @ joltages
        #     except np.linalg.LinAlgError:
        #         pass
        #     else:
        #         if p.min() < 0:
        #             continue
                    
        #         n = p.sum().round(2).round()
        #         if best is None or n < best:
        #             best = n


        x, _, _, _ = np.linalg.lstsq(M, joltages)

        print(x)

        print(np.sum(x[x > 0]))
        


        #print(best)

    #         total_presses += sum(best_path)

    #     print(total_presses)

    #     return










def combine_presses(a : dict[int, int], b : dict[int, int]):
    assert len(a) == len(b)
    #return {k : a.get(k, 0) + b.get(k, 0) for k in range(max(max(list(a)), max(list(b)))+1)}
    return tuple([ai+bi for ai, bi in zip(a, b)])
    
def rc(n : int, values : list[int], n_buttons : int):
    output : list[int] = [0]*n_buttons
    #d = {v : 0 for v in values}
    v = values[0]
    if len(values) == 1:
        output[v] += n
        yield output
        return None
    
    for j in range(0, n+1):
        for rc_output in rc(n-j, values[1:], n_buttons):
            di = output.copy()
            di[v] += j
            for i, counts in enumerate(rc_output):
                di[i] += counts
            yield di

def calculate_joltage(N : int, buttons : list[tuple[int]], pressed_buttons : tuple[int]):
    assert len(pressed_buttons) == len(buttons)
    counters = [0]*N
    for i, counts in enumerate(pressed_buttons):
        for index in buttons[i]:
            counters[index] += counts

    return counters


def valid_joltage(reference_joltages : list[int], joltages : dict[int, int]):
    return all(joltages[i] <= reference_joltages[i] for i in range(len(reference_joltages)))

@lru_cache(maxsize=2048)
def recurse_find_path(buttons : tuple[tuple[int]], joltages : tuple[int], button_presses : tuple[int], i : int = 0) -> list[int]:
    N = len(joltages)
    if i == len(joltages):
        return button_presses
    
    # if joltages[i] == 0:
    #     print('=0, go to next')
    #     return recurse_find_path(buttons, joltages, path, i+1)

    current_joltages = calculate_joltage(N, buttons, button_presses)
    joltage_delta = joltages[i] - current_joltages[i]

    if joltage_delta == 0:
        #print(f'nothing to do on joltage {i}, go to next')
        return recurse_find_path(buttons, joltages, button_presses, i+1)

    available_buttons = [bi for bi, button in enumerate(buttons) if i in button]
    
    new_paths = []

    #print(' '*i + f'Available buttons : {available_buttons} to get joltage {i} from {current_joltages[i]} to {joltages[i]}')


    joltage_delta 

    for presses in rc(joltage_delta, available_buttons, len(buttons)):
        #print(' '*i + "  " + str(presses))
        #print(' '*i + " +" + str(button_presses))
        new_presses = combine_presses(button_presses, presses)
        #print(' '*i + "c:" + str(new_presses))
    #for path_suffix in combinations_with_replacement(available_buttons, joltage_delta):
        #new_path = list(path) + list(path_suffix)
        #print(path_suffix)
        new_joltages = calculate_joltage(N, buttons, new_presses)

        if not valid_joltage(joltages, new_joltages):
            continue
        #print(f'New path : {new_path} -> {new_joltages}')

        #new_path.sort()
        new_completed_path = recurse_find_path(buttons, joltages, new_presses, i+1)
        if new_completed_path is not None:
        #print(f'New path : {new_completed_path}')
            new_paths.append(new_completed_path)
        

    new_paths.sort(key=lambda path : sum(path))
    #print(' '*i + f'Output paths : {new_paths}')

    if len(new_paths) == 0:
        return None
    
    return new_paths[0]

if __name__ == '__main__':
    main()