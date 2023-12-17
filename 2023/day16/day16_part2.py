from sys import argv
import numpy as np
from enum import Enum
from colorama import Fore, Style
from tqdm import tqdm
from time import sleep


EMPTY = 0
VERTICAL_SPLITTER = 1 << 0
HORIZONTAL_SPLITTER = 1 << 1
MIRROR_135 = 1 << 2
MIRROR_45 = 1 << 3

NORTH = 1 << 0
SOUTH = 1 << 1
WEST = 1 << 2
EAST = 1 << 3

ELEMENT_MAP = {
    '.' : EMPTY,
    '|' : VERTICAL_SPLITTER,
    '-' : HORIZONTAL_SPLITTER,
    '/' : MIRROR_45,
    '\\' : MIRROR_135
}
ELEMENT_MAP_INV = {v : k for k, v in ELEMENT_MAP.items()}

EMPTY_MAP = {
    EMPTY : ' ',
    NORTH : '┃',
    SOUTH : '┃',
    NORTH | SOUTH : '┃',
    EAST : '━',
    WEST : '━',
    EAST | WEST : '━',
    NORTH | EAST : '╋',
    NORTH | WEST : '╋',
    SOUTH | EAST : '╋',
    SOUTH | WEST : '╋',
    EAST | WEST | NORTH : '╋',
    EAST | WEST | SOUTH : '╋',
    NORTH | SOUTH | WEST : '╋',
    NORTH | SOUTH | EAST : '╋',
    NORTH | SOUTH | EAST | WEST : '╋',
}

class Position:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
    
    def __add__(self, o):
        return Position(self.x + o.x, self.y + o.y)

    def idx(self):
        return self.y, self.x

    def __repr__(self) -> str:
        return f'({self.x:+d},{self.y:+d})'

class Direction(Position):
    def horizontal(self):
        return self.x != 0

    def rotate_90(self):
        return Direction(-self.y, self.x)
    
    def rotate_270(self):
        return Direction(self.y, -self.x)

    def val(self):
        return {
            (0, 1) : NORTH,
            (0, -1) : SOUTH,
            (1, 0) : EAST,
            (-1, 0) : WEST
        }[(self.x, self.y)]

def parse_contraption(data):
    return np.array([[ELEMENT_MAP[x] for x in line] for line in data.split('\n') if line != ''])

def iterate_light_path(matrix, p):
    current_position = matrix[p[0].idx()]
    if current_position == EMPTY or \
        (current_position == VERTICAL_SPLITTER and not p[1].horizontal()) or\
        (current_position == HORIZONTAL_SPLITTER and p[1].horizontal()):
        output = [(p[0] + p[1], p[1])]
    elif current_position == VERTICAL_SPLITTER:
        output = [
            (p[0] + Direction(0, 1), Direction(0, 1)),
            (p[0] + Direction(0, -1), Direction(0, -1))]
    elif current_position == HORIZONTAL_SPLITTER:
        output = [
            (p[0] + Direction(1, 0), Direction(1, 0)),
            (p[0] + Direction(-1, 0), Direction(-1, 0))]

    elif current_position in [MIRROR_135, MIRROR_45]:
        if (current_position == MIRROR_45) ^ p[1].horizontal():
            new_direction = p[1].rotate_90()
        else:
            new_direction = p[1].rotate_270()
        output = [(p[0] + new_direction, new_direction)]
    else:
        raise RuntimeError()
    return output

def simulate_light_path(matrix, start):
    energized_matrix = np.zeros_like(matrix)
    positions_directions = [start]
    while True:
        new_positions_directions = []
        for pds in positions_directions:
            energized_matrix[pds[0].idx()] |= pds[1].val()
            new_positions_directions += iterate_light_path(matrix, pds)
            for npds in new_positions_directions:
                if not (0 <= npds[0].x < matrix.shape[1]) \
                    or not (0 <= npds[0].y < matrix.shape[0]) or \
                        energized_matrix[npds[0].idx()] & npds[1].val():
                    new_positions_directions.remove(npds)

        # print()
        # print()
        # print_matrix(matrix, energized_matrix, start[0])
        # input()
        if len(new_positions_directions) == 0:
            break
        positions_directions = new_positions_directions

    return energized_matrix


def print_matrix(matrix, energize_matrix, start):
    _str = ''
    for y, (ml, eml) in enumerate(zip(matrix, energize_matrix)):
        for x, (mx, emx) in enumerate(zip(ml, eml)):
            if x == start.x and y == start.y:
                _str += Style.RESET_ALL + Fore.RED + Style.BRIGHT
            elif emx > 0:
                if mx == EMPTY:
                    _str += Style.RESET_ALL + Fore.WHITE + Style.DIM
                else:
                    _str += Style.RESET_ALL + Fore.CYAN + Style.BRIGHT
            else:
                _str += Style.RESET_ALL + Fore.LIGHTBLACK_EX + Style.DIM
            if emx == 0:
                _str += ' '
            elif mx == EMPTY:
                _str += EMPTY_MAP[energize_matrix[y, x]]
            else:
                _str += str(ELEMENT_MAP_INV[mx])
        _str += '\n'
    print(_str)
    print(Style.RESET_ALL)

def starts(matrix):
    outputs = []
    for d in [-1, 1]:
        for x in range(matrix.shape[1]):
            outputs.append((Position(x, 0 if d > 0 else matrix.shape[0]-1), Direction(0, d)))
        for y in range(matrix.shape[0]):
            outputs.append((Position(0 if d > 0 else matrix.shape[1]-1, y), Direction(d, 0)))
    return outputs


def main():
    file = argv[1]
    with open(file) as f:
        data = f.read()
        matrix = parse_contraption(data)
        _max = None
        for start in tqdm(starts(matrix)):
            energize_matrix = simulate_light_path(matrix, start)
            N = np.sum(energize_matrix != EMPTY)
            if _max is None or N > _max:
                _max = N
        print(_max)

if __name__ == '__main__':
    main()