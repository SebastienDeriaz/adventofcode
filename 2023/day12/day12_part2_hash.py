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


# def positions_match_conditions(positions, conditions, counts, broken_groups):
#     output_A = True
#     for p, c in zip(positions, counts):
#         if OPERATIONAL in conditions[p:p+c]:
#             output_A = False
#             break
#     for b, c in broken_groups:
#         if 

#     pos_string = positions_string(len(conditions), positions, counts)
#     assert len(pos_string) == len(conditions)
#     output_B = all([c == UNKNOWN or c == p for c, p in zip(conditions, pos_string)])
#     if output_B != output_A:
#         print(f'Positions : {positions}')
#         print(f'Counts : {counts}')
#         print(f'Conditions : {conditions}')
#         input(f'pos_string : {pos_string}')
#     return output_B

perf_hist =  []
perf_hist_A = []


def _hash(N : int, positions : list, counts : list):
    n = 0
    for p, c in zip(positions, counts):
        n |= (2**c-1) << p
    return n

def disp_hash(N, hash):
    return f'{hash:0{N}b}'[::-1]

def try_all(N : int, broken_hash : int, operational_hash : int, positions, counts, i):
    if i == 0:
        _min = 0
    else:
        _min = positions[i-1] + counts[i-1] + 1

    # Try all positions of the ith one
    if i == len(counts) - 1:
        # Last one
        _max = N - counts[i]
    else:
        _max = N - (sum(counts[i+1:]) + (len(counts)-i))
        _max = max(_max, _min)

    if _max >= _min:
        _rng = range(_max, _min-1, -1)
        for k in _rng:
            positions[i] = k
            new_hash = _hash(N, positions, counts)

            # print(f'new         : {disp_hash(N, new_hash)}')
            # print(f'broken      : {disp_hash(N, broken_hash)}')
            # print(f'operational : {disp_hash(N, operational_hash)}')
            input()
            if broken_hash & ~new_hash > 0:
                continue
            
            if operational_hash & new_hash > 0:
                continue

            if i == len(positions) - 1:
                N += 1
            else:
                try_all(N, broken_hash, operational_hash, positions, counts, i+1)


            # pos_max = k + counts[i] + 1
            # if i == 0:
            #     pos_min = 0
            # else:
            #     pos_min = _min

            # if i < len(counts) - 5:
            #     print(f'{conditions} {",".join([str(c) for c in counts])}')
            #     print(new_conditions)

            # if operational_hash & _hash(N, [k], [counts[i]]) > 0:
            #     # Skip it, it's not even possible
            #     continue
            

            # if any([(c == BROKEN and nc == OPERATIONAL) for (c, nc) in zip(conditions[pos_min:pos_max], new_conditions[pos_min:pos_max])]):
            #     continue

    # if i == len(positions) - 1:
    #     stop = perf_counter_ns()
    #     perf_hist.append(stop - start)

    return N

def count_arangements(conditions, counts):
    N = len(conditions)
    p = N - sum(counts) - len(counts) + 1
    positions = []
    for i, c in enumerate(counts):
        positions.append(p)
        p += c + 1

    broken_hash = sum([2**i for i, c in enumerate(conditions) if c == BROKEN])
    operational_hash = sum([2**i for i, c in enumerate(conditions) if c == OPERATIONAL])

    return try_all(len(conditions), broken_hash, operational_hash, positions, counts, 0)


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
            # f = n2 // n1
            # #nuf = n1 * f**(UNFOLD_FACTOR-1)
            # nuf = n5
            # N += nuf

        print(f'Total : {N}')
        #print(f'mean : {np.mean(perf_hist)*1e-3:.1f} us, std : {np.std(perf_hist)*1e-3:.1f} us')


if __name__ == '__main__':
    main()