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
    print(f'{pos_string} == {conditions} ({output})')
    return output


def try_all(conditions, positions, counts, i):
    # Try all positions of the ith one
    # TODO : FIx min and max, they should never depend on conditions[i+...] because those aren't correct at the moment   _max = sum(counts[i:]) + (len(counts)-i-1-1) 
    _min = 0 if i == 0 else positions[i-1] + counts[i-1] + 1
    print(f'{"  "*i}{i=} {_min} to {_max}')
    N = 0
    # if i == 0 and positions_match_conditions(positions, conditions, counts):
    #     N += 0
    if _max >= _min:
        for k in range(_max, _min-1, -1):
            print(f'{"  "*i}Move {i}->{k}')
            positions[i] = k
            if i < len(positions) - 1:
                N += try_all(conditions, positions, counts, i+1)
            else:
                print('  '*i, end='')
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

    print(positions)

    return try_all(conditions, positions, counts, 0)





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
        for line in lines[1:2]:
            parsed_line = parse_line(line)
            print(parsed_line)
            n = count_arangements(*parsed_line)
            N += n
        print(f'Total : {N}')

if __name__ == '__main__':
    main()