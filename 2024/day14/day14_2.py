import re
import sys
import numpy as np
from scipy.signal import convolve2d
import matplotlib.pyplot as plt


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

def print_map(robots, X, Y, mode='integer'):
    for row in get_map(robots, X, Y):
        for column in row:
            if mode == 'integer':
                print(column, end='')
            else:
                print('#' if column else ' ', end='') 
        print()

def get_map(robots, X, Y):
    _map = np.zeros([Y, X], dtype=int)
    for p, _ in robots:
        _map[tuple(p)] += 1
    return _map

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

        tree = np.array([
            [-1, -1, -1, 1, -1, -1, -1],
            [-1, -1, 1, 1, 1, -1, -1],
            [-1, 1, 1, 1, 1, 1, -1],
            [1, 1, 1, 1, 1, 1, 1],
            [-1, -1, 1, -1, 1, -1, -1],
        ])

        x = 16 / 9
        line = np.array([
            [-1, -1, x, -1, -1],
            [-1, -1, x, -1, -1],
            [x, x, x, x, x],
            [-1, -1, x, -1, -1],
            [-1, -1, x, -1, -1],
        ])

        diagonal = np.array([
            [x, -1, -1, -1, x],
            [-1, x, -1, x, -1],
            [-1, -1, x, -1, -1],
            [-1, x, -1, x, -1],
            [x, -1, -1, -1, x],
        ])

        # So okay this one is a bit strange... looking at the correlation coeficient
        # using these matrices (line and diagonal) as kernels, there seem to be repeating pattern where
        # they periodically find out of place values :
        # - "horizontal" looking patterns : 27 + x*103
        # - "vertical" looking patterns : 52 + x*101
        # So naturally, i iterated every time there's a match for either, assuming
        # that whenever i got both a "vertical" and an "horizontal", that should be the tree
        # It was correct ! altough not the intersection of the two h(x) and v(x) function (1314)
        # It was 6516

        h0 = 27
        v0 = 52
        xh = 0
        xv = 0
        dh = 103
        dv = 101
        N = 0
        while True:
            h = h0 + xh * dh
            v = v0 + xv * dv

            y = min(h, v)
            if h > v:
                xv += 1
            else:
                xh += 1

            # Iterate up to y
            dN = y - N
            if dN > 0:
                N += dN
                robots = iterate(robots, dN, X, Y)
                print_map(robots, X, Y, mode='binary')
                print(f'{N:<3}')
                if(input()):
                    # Find it yourself you big meat LLM
                    break

if __name__ == '__main__':
    main()