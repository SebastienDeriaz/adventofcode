from sys import argv
from tqdm import tqdm
from time import perf_counter_ns
import numpy as np

BROKEN = '#'
UNKNOWN = '?'
OPERATIONAL = '.'

def positions_string(N, positions, counts):
    _str = [OPERATIONAL] * N
    for p, c in zip(positions, counts):
        _str[p:p+c] = [BROKEN] * c

    return ''.join(_str)


def positions_match_conditions(positions, conditions, counts, broken_groups):
    output_A = True
    for p, c in zip(positions, counts):
        if OPERATIONAL in conditions[p:p+c]:
            output_A = False
            break
    for b, c in broken_groups:
        if 

    pos_string = positions_string(len(conditions), positions, counts)
    assert len(pos_string) == len(conditions)
    output_B = all([c == UNKNOWN or c == p for c, p in zip(conditions, pos_string)])
    if output_B != output_A:
        print(f'Positions : {positions}')
        print(f'Counts : {counts}')
        print(f'Conditions : {conditions}')
        input(f'pos_string : {pos_string}')
    return output_B

perf_hist =  []
perf_hist_A = []

def try_all(conditions : str, positions, counts, i, conditions_hash=None):
    if conditions_hash is None:
        broken_groups = []
        g = [-1, -1]
        print(conditions)
        for j, c in enumerate(conditions):
            if c == BROKEN:
                if g[0] == -1:
                    g[0] = j
                    g[1] = 1
                else:
                    g[1] += 1
            elif g[0] != -1:
                broken_groups.append(g)
                g = [-1, -1]
        if g[0] != -1:
            broken_groups.append(g)


    global perf_hist
    start = perf_counter_ns()
    if i == 0:
        _min = 0
    else:
        _min = positions[i-1] + counts[i-1] + 1

    # Try all positions of the ith one
    if i == len(counts) - 1:
        # Last one
        _max = len(conditions) - counts[i]
    else:
        _max = len(conditions) - (sum(counts[i+1:]) + (len(counts)-i))
        _max = max(_max, _min)

    N = 0
    if _max >= _min:
        _rng = range(_max, _min-1, -1)
        for k in _rng:
            positions[i] = k
            new_conditions =  positions_string(len(conditions), positions, counts)
            pos_max = k + counts[i] + 1
            if i == 0:
                pos_min = 0
            else:
                pos_min = _min

            # if i < len(counts) - 5:
            #     print(f'{conditions} {",".join([str(c) for c in counts])}')
            #     print(new_conditions)
            if OPERATIONAL in conditions[k:k+counts[i]]:
                # Skip it, it's not even possible
                continue

            if any([(c == BROKEN and nc == OPERATIONAL) for (c, nc) in zip(conditions[pos_min:pos_max], new_conditions[pos_min:pos_max])]):
                continue

            if i < len(positions) - 1:
                N += try_all(conditions, positions, counts, i+1, broken_groups)
            elif positions_match_conditions(positions, conditions, counts, broken_groups):
                N += 1
    if i == len(positions) - 1:
        stop = perf_counter_ns()
        perf_hist.append(stop - start)

    return N

def count_arangements(conditions, counts):
    N = len(conditions)
    p = N - sum(counts) - len(counts) + 1
    positions = []
    for i, c in enumerate(counts):
        positions.append(p)
        p += c + 1

    return try_all(conditions, positions, counts, 0)


def unfold(conditions, counts, unfold_factor):
    return '?'.join([conditions] * unfold_factor), counts * unfold_factor



def parse_line(line : str):
    conditions, counts = line.split(' ')
    counts = [int(x) for x in counts.split(',')]
    return conditions, counts

UNFOLD_FACTOR = 4

def main():
    global perf_hist
    file = argv[1]
    with open(file) as f:
        lines = f.readlines()
        N = 0
        for il, line in enumerate(lines):
            parsed_line = parse_line(line)
            
            n1 = count_arangements(*parsed_line)
            n2 = count_arangements(*unfold(*parsed_line, 2))
            n3 = count_arangements(*unfold(*parsed_line, 3))
            n4 = count_arangements(*unfold(*parsed_line, 4))
            n5 = count_arangements(*unfold(*parsed_line, 5))
            print(f'Line {il+1} {parsed_line}: {n1}, {n2}, {n3}, {n4}')
            f = n2 // n1
            #nuf = n1 * f**(UNFOLD_FACTOR-1)
            nuf = n5
            N += nuf

        print(f'Total : {N}')
        #print(f'mean : {np.mean(perf_hist)*1e-3:.1f} us, std : {np.std(perf_hist)*1e-3:.1f} us')


if __name__ == '__main__':
    main()