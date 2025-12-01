import sys


EMPTY = '.'
FULL = '#'

def parse_file(file):
    keys = []
    locks = []
    with open(file) as f:
        data = f.read()

        PATTERN = '((?:[\.#]+\n)+)'

        for key_lock in data.split('\n\n'):

            lines = key_lock.split('\n')
            is_lock = lines[0].count(FULL) == len(lines[0])
            values = [-1] * len(lines[0])
            for l in lines:
                for i, c in enumerate(l):
                    if c == FULL:
                        values[i] += 1

            if is_lock:
                locks.append(values)
            else:
                keys.append(values)

    return locks, keys

def match(lock, key, N):
    return all([l+k < N for l, k in zip(lock, key)])


def main():
    locks, keys = parse_file(sys.argv[1])

    N = 6

    matches = 0
    for l in locks:
        for k in keys:
            m = match(l, k, N)
            if m:
                matches += 1
    print(matches)

if __name__ == '__main__':
    main()



                
