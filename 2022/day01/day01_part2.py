import sys


def main():
    file = sys.argv[1]

    with open(file) as f:
        data = f.read()


    elves = [[int(y) for y in x.split('\n')] for x in data.split('\n\n')]

    total_calories = [sum(x) for x in elves]

    total_calories.sort(reverse=True)

    print(sum(total_calories[:3]))



if __name__ == '__main__':
    main()