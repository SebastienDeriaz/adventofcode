conditions = '???.###'
counts = [1, 1, 3]

#conditions = '?#?#?#?#?#?#?#?'
#counts = [1, 3, 1, 6]

BROKEN = '#'
OPERATIONAL = '.'
UNKNOWN = '?'

N = len(conditions)


def positions_string(N, positions, counts):
    _str = [OPERATIONAL] * N
    for p, c in zip(positions, counts):
        _str[p:p+c] = [BROKEN] * c

    return ''.join(_str)




p = N - sum(counts) - len(counts) + 1
positions = []
for c in counts:
    positions.append(p)
    p += c + 1

print(positions)



def positions_match_conditions(positions, conditions, counts):
    pos = positions_string(len(conditions), positions, counts)
    print(f'{pos} == {conditions}')
    return all([c == '?' or c == p for c, p in zip(conditions, pos)])

def try_all(conditions, positions, counts, i):
    # Try all positions of the ith one
    _max = positions[i]
    _min = 0 if i == 0 else positions[i-1] + counts[i-1] + 1
    N = 0
    print(f'Move {i}')
    if i == 0 and positions_match_conditions(positions, conditions, counts):
        N += 0
    if _max >= _min:
        for k in range(_min, _max+1):
            print(f'  at {k}')
            if positions[i] != k:
                if positions_match_conditions(positions, conditions, counts):
                    print(f'  -> match !')
                    N += 1
                if i < len(positions) - 1 and k > 0:
                    N += try_all(conditions, positions, counts, i+1)
    return N



try_all(conditions, positions, counts, 0)