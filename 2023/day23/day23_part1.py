from sys import argv
import numpy as np
import colorama


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
        (Vec2D(-1, 0),[GROUND]),
        (Vec2D(1, 0),[EAST_SLOPE, GROUND]),
        (Vec2D(0, 1),[SOUTH_SLOPE, GROUND]),
        (Vec2D(0, -1),[WEST_SLOPE, GROUND])
    ]

    outputs = []

    for offset, accept in neighbors:
        p = position + offset
        if p.valid_range(map) and map[p.idx()] in accept:
            outputs.append(p)

    return outputs


def print_map(map : np.array):
    for line in map:
        for x in line:
            if x == PATH:
                print(colorama.Style.BRIGHT + colorama.Fore.CYAN, end='')
            else:
                print(colorama.Style.DIM + colorama.Fore.LIGHTBLACK_EX, end='')
            print(SYMBOL_MAP_INV[x], end='')
        print()
    print(colorama.Style.RESET_ALL)



def find_longest_route(map : np.array, start : Vec2D):
    path_map = map.copy()
    p = start
    N = 0
    while True:
        path_map[p.idx()] = PATH
        N += 1

        next_ps = find_adjacent(path_map, p)
        if len(next_ps) == 1:
            # There's only one path to go to
            p = next_ps[0]
        elif len(next_ps) == 0:
            # There's no more path to go
            break
        else:
            # Recursively search the paths
            lengths = []
            #if i == 1:
            for next_p in next_ps:
                lengths.append(find_longest_route(path_map, next_p))
            # Choose the longest path
            n, p, new_map = max(lengths, key=lambda x : x[0])
            path_map[new_map == PATH] = PATH
            N += n - 1
    return N, p, path_map


def main():
    file = argv[1]
    with open(file) as f:
        data = f.read()
        map = parse_map(data)

        N, _, new_map = find_longest_route(map, Vec2D(1, 0))
        print_map(new_map)
        print(N - 1) # Remove one because the first point is "S"

if __name__ == '__main__':
    main()