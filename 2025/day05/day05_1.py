from sys import argv

SEPARATOR = '-'

def main():
    file = argv[1]

    ranges = []
    available_ingredients = set()
    with open(file) as f:
        contents = f.read()

        for line in contents.split('\n'):
            if not line:
                continue
            if SEPARATOR in line:
                ranges.append(tuple([int(x) for x in line.split(SEPARATOR)]))
            else:
                available_ingredients.add(int(line))
                #available_ingredients.append(int(line))

    # print(f'{len(ranges)} ranges')
    # print(f'{len(available_ingredients)} ingredients')

    fresh_count = 0
    for ingredient in available_ingredients:
        for a, b in ranges:
            if a <= ingredient <= b:
                fresh_count += 1
                break

    print(fresh_count)
        


if __name__ == '__main__':
    main()