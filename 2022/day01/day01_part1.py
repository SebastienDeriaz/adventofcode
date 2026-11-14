import sys


def main():
    file = sys.argv[1]

    with open(file) as f:
        data = f.read()


    elves = [[int(y) for y in x.split('\n')] for x in data.split('\n\n')]

    total_calories = [sum(x) for x in elves]

    print(max(total_calories))



if __name__ == '__main__':
    main()