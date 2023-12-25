from sys import argv
import numpy as np
import colorama

import sys

sys.setrecursionlimit(10_000)


class Vec2D:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    def idx(self):
        return (self.y, self.x)

    def __add__(self, o):
        return Vec2D(self.x + o.x, self.y + o.y)

    def __sub__(self, o):
        return Vec2D(self.x - o.x, self.y - o.y)

    def __eq__(self, __o: object) -> bool:
        return self.x == __o.x and self.y == __o.y

    def __repr__(self) -> str:
        return f'({self.x},{self.y})'

    def rotate_90(self):
        return Vec2D(-self.y, self.x)

    def rotate_270(self):
        return Vec2D(self.y, -self.x)

    def valid_range(self, matrix):
        return 0 <= self.x < matrix.shape[1] and 0 <= self.y < matrix.shape[0]


GROUND = 0
FOREST = 1
SOUTH_SLOPE = 2
WEST_SLOPE = 3
EAST_SLOPE = 4
PATH = 5



SYMBOL_MAP = {
    '.' : GROUND,
    '#' : FOREST,
    '>' : EAST_SLOPE,
    '<' : WEST_SLOPE,
    'v' : SOUTH_SLOPE,
    'O' : PATH,
}

SYMBOL_MAP_INV = {
    v : k for k, v in SYMBOL_MAP.items()
}

def parse_map(data):
    return np.array([[SYMBOL_MAP[x] for x in line] for line in data.split('\n') if line != ''])



def find_adjacent(map, position : Vec2D):
    neighbors = [
        Vec2D(-1, 0),
        Vec2D(1, 0),
        Vec2D(0, 1),
        Vec2D(0, -1)
    ]

    outputs = []

    for offset in neighbors:
        p = position + offset
        if p.valid_range(map) and map[p.idx()] not in [FOREST, PATH]:
            outputs.append(p)

    return outputs

def fill_matrix(map : np.array, start : Vec2D, end : Vec2D, counter_map : np.array = None, value : int = 0):
    if counter_map is None:
        counter_map = np.zeros_like(map)

    p = start
    counter_map[p.idx()] = value
    map[p.idx()] = PATH

    next_ps = find_adjacent(map, p)
    for next_p in next_ps:
        if counter_map[next_p.idx()] > value or map[next_p.idx()] == PATH:
            # Ignore it
            continue
        else:
            fill_matrix(map, next_p, end, counter_map, value + 1)

    return np.max(counter_map)



def main():
    file = argv[1]
    with open(file) as f:
        data = f.read()
        map = parse_map(data)
        end = Vec2D(map.shape[1]-2, map.shape[0]-1)
        counter_map = fill_matrix(map, Vec2D(1, 0), end)
        print(np.max(counter_map))

if __name__ == '__main__':
    main()