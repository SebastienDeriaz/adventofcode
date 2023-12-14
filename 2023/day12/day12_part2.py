from sys import argv


BROKEN = '#'
UNKNOWN = '?'
OPERATIONAL = '.'

def positions_string(N, positions, counts):
    _str = [OPERATIONAL] * N
    for p, c in zip(positions, counts):
        _str[p:p+c] = [BROKEN] * c

    return ''.join(_str)

def positions_match_conditions(positions, conditions, counts):
    pos_string = positions_string(len(conditions), positions, counts)
    assert len(pos_string) == len(conditions)
    output = all([c == '?' or c == p for c, p in zip(conditions, pos_string)])
    #print(f'{pos_string} == {conditions} ({output})')
    return output


def try_all(conditions, positions, counts, i):

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

    #print(f'{"  "*i}{i=} {_min} to {_max}')
    N = 0
    if _max >= _min:
        for k in range(_max, _min-1, -1):
            #print(f'{"  "*i}Move {i}->{k}')
            if OPERATIONAL in conditions[k:k+counts[i]]:
                # Skip it, it's not even possible
                continue
            
            new_conditions = positions_string(len(conditions), positions[:i] + [k] + positions[i+1:], counts)
            pos_max = k + counts[i] - 1
            if any([c == BROKEN and nc == OPERATIONAL for c, nc in zip(conditions[:pos_max], new_conditions[:pos_max])]):
                continue

            positions[i] = k
            if i < len(counts) - 3:
                print(conditions)
                print(positions_string(len(conditions), positions, counts))

            if i < len(positions) - 1:
                N += try_all(conditions, positions, counts, i+1)
            else:
                if positions_match_conditions(positions, conditions, counts):
                    N += 1

    return N

def count_arangements(conditions, counts):
    N = len(conditions)
    p = N - sum(counts) - len(counts) + 1
    positions = []
    for i, c in enumerate(counts):
        positions.append(p)
        p += c + 1

    print(positions_string(N, positions, counts))
    return try_all(conditions, positions, counts, 0)


def unfold(conditions, counts, unfold_factor):
    return '?'.join([conditions] * unfold_factor), counts * unfold_factor



def parse_line(line : str):
    conditions, counts = line.split(' ')
    counts = [int(x) for x in counts.split(',')]
    return conditions, counts

UNFOLD_FACTOR = 5

def main():
    file = argv[1]
    with open(file) as f:
        lines = f.readlines()
        N = 0
        for line in lines:
            parsed_line = parse_line(line)
            parsed_line = unfold(*parsed_line, UNFOLD_FACTOR)
            print(parsed_line)
            n = count_arangements(*parsed_line)
            N += n
        print(f'Total : {N}')

if __name__ == '__main__':
    main()