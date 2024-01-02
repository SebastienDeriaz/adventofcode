from sys import argv

BROKEN = '#'
UNKNOWN = '?'
OPERATIONAL = '.'

def positions_string(N, positions, counts):
    _str = [OPERATIONAL] * N
    for p, c in zip(positions, counts):
        _str[p:p+c] = [BROKEN] * c

    return ''.join(_str)

perf_hist =  []
perf_hist_A = []


def hash_string(N, broken_hash : int, operational_hash : int = None):
    output = ''
    for i in range(N):
        b = (broken_hash >> i) & 1
        if b == 1:
            output += BROKEN
        elif operational_hash is not None and ((operational_hash >> i) & 1) == 0:
            output += UNKNOWN
        else:
            output += OPERATIONAL
    return output

def _hash(N : int, positions : list, counts : list):
    n = 0
    for p, c in zip(positions, counts):
        n |= (2**c-1) << p
    return n

def disp_hash(N, hash):
    return f'{hash:0{N}b}'[::-1]

call_counter = 0

hash_counter = 0

def try_all(N : int, broken_hash : int, operational_hash : int, positions, counts, i):
    global hash_counter
    global call_counter
    call_counter += 1
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

    counter = 0

    # if i < 2:
    #     print(f'positions[i-1] : {positions[i-1]}, counts[i-1] {counts[i-1]}')
    # print(f'{i} {_min}->{_max}')
    if _max >= _min:
        _rng = range(_max, _min-1, -1)
        for k in _rng:
            positions[i] = k
            new_hash = _hash(N, positions[:i+1], counts)
            mask = 2**(k + counts[i]) - 1
            
            # print(f'Operational hash  : {disp_hash(N, operational_hash)}')
            # print(f'{hash_counter:05} New hash  : {disp_hash(N, new_hash)}')
            hash_counter += 1

            _continue = False
            if (broken_hash & ~new_hash) & mask > 0:
                # print(' skip A')
                _continue = True
            
            if (operational_hash & new_hash) & mask > 0 and _continue == False:
                # print(' skip B')
                _continue = True

            if not _continue:
                # print(' keep')
                pass
            if _continue:
                continue


            if i == len(positions) - 1:
                counter += 1
            else:
                counter += try_all(N, broken_hash, operational_hash, positions, counts, i+1)

    return counter

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

UNFOLD_FACTOR = 5

def main():
    global perf_hist
    global call_counter
    file = argv[1]
    with open(file) as f:
        lines = f.readlines()
        N = 0
        for i, line in enumerate(lines):
            print(f'Line {i+1}')
            parsed_line = parse_line(line)

            unfolded_line = unfold(*parsed_line, UNFOLD_FACTOR)
            n = count_arangements(*unfolded_line)
            print(f'  {n}')
                
            N += n

            #print(f'Line {il+1} {parsed_line}: {n1}, {n2}, {n3}, {n4}')
            #nuf = n5
            #N += nuf

        print(f'Total : {N}')
        print(f'{call_counter=}')
        #print(f'mean : {np.mean(perf_hist)*1e-3:.1f} us, std : {np.std(perf_hist)*1e-3:.1f} us')


if __name__ == '__main__':
    main()