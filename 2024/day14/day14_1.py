import re
import sys
import numpy as np

def parse_data(data):
    PATTERN = 'p=(\d+),(\d+) v=([\-\d]+),([\-\d]+)'
    robots = []
    for values in re.findall(PATTERN, data):
        x, y, vx, vy = [int(x) for x in values]
        robots.append((np.array([y, x]), np.array([vy, vx])))

    return robots


def iterate(robots, N, X, Y):
    new_robots = []
    for p, v in robots:
        p2 = p + N * v
        p2[0] = np.mod(p2[0], Y)
        p2[1] = np.mod(p2[1], X)
        new_robots.append((p2, v))
    
    return new_robots

def print_map(robots, X, Y):
    _map = np.zeros([Y, X], dtype=int)
    for p, _ in robots:
        _map[tuple(p)] += 1

    for row in _map:
        for column in row:
            print(column, end='')
        print()

def calculate_safety_factor(robots, X, Y):
    quadrants = {
        (-1, -1) : 0,
        (-1, 1) : 0,
        (1, -1) : 0,
        (1, 1) : 0
    }
    for p, _ in robots:
        q = np.sign(p - (np.array([Y, X], dtype=int)-1)//2)
        if np.prod(q) != 0:
            quadrants[tuple(q)] += 1

    return np.prod(list(quadrants.values()))


def main():
    file, X, Y = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    with open(file) as f:
        data = f.read()
        robots = parse_data(data)

        N = 100
        robots_100 = iterate(robots, N, X, Y)

        print(calculate_safety_factor(robots_100, X, Y))


if __name__ == '__main__':
    main()