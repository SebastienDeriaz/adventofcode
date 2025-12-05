from sys import argv

SEPARATOR = '-'

# 345943501248633 wrong

def main():
    file = argv[1]

    ranges = []
    with open(file) as f:
        contents = f.read()

        for line in contents.split('\n'):
            if not line:
                continue
            if SEPARATOR in line:
                ranges.append(tuple([int(x) for x in line.split(SEPARATOR)]))
                #available_ingredients.append(int(line))

    # Simplify the ranges

    finished = False
    while not finished:
        for i, (a, b) in enumerate(ranges):
            for j, (c, d) in enumerate(ranges):
                if j == i:
                    continue
                if a == b and c <= a <= d:
                    # Remove a-b
                    #print(f'remove {a}-{b}')
                    ranges.remove((a, b))
                    break
                elif b <= d and b >= c:
                    #print(f'Fuse {a}-{b} and {c}-{d}')
                    # Fuse them
                    ranges.remove((a, b))
                    ranges.remove((c, d))
                    ranges.append((min(a, b, c, d), max(a, b, c, d)))
                    break
            else:
                continue
            break
        else:
            finished = True
            #continue

    total = 0
    for a, b in ranges:
        total += b - a + 1

    print(total)

    

if __name__ == '__main__':
    main()