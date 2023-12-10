from sys import argv
import numpy as np
from enum import Enum


NORTH = (1 << 0) # 1
SOUTH = (1 << 1) # 2
EAST =  (1 << 2) # 4
WEST =  (1 << 3) # 8
GROUND = -1
STARTING_POSITION = 0

XY_TO_DIRECTION = {
    (0, -1) : NORTH,
    (0, 1) : SOUTH,
    (-1, 0) : WEST,
    (1, 0) : EAST
}

DIRECTION_TO_XY = {x : k for k, x in XY_TO_DIRECTION.items()}

SYMBOLS = {
    '|' : NORTH | SOUTH,
    '-' : EAST | WEST,
    'L' : NORTH | EAST,
    'J' : NORTH | WEST,
    '7' : SOUTH | WEST,
    'F' : SOUTH | EAST,
    '.' : -1,
    'S' : 0,
}


def find_start_pipes(matrix):
    # Find the start
    yx = np.array(np.where(matrix == STARTING_POSITION))
    # Find the start pipes
    print(f'Start at ({yx[1,0]}, {yx[0,0]})')
    positions = []
    directions = []
    for dx, dy in XY_TO_DIRECTION:
        y = dy + yx[0, 0]
        x = dx + yx[1, 0]
        if y < 0 or y >= matrix.shape[0] or x < 0 or x >= matrix.shape[1]:
            continue
        new_position = matrix[y,x]
        if new_position & XY_TO_DIRECTION[(-dx, -dy)] > 0 and matrix[y,x] > 0:
            positions.append((x, y))
            directions.append(new_position & (~XY_TO_DIRECTION[(-dx, -dy)]))

    return positions, directions

def iterate(matrix, position, direction):
    d = DIRECTION_TO_XY[direction]
    input_direction = XY_TO_DIRECTION[tuple(-x for x in d)]
    new_position = (position[0] + d[0], position[1] + d[1])
    new_direction = matrix[new_position[::-1]] & (~input_direction)
    return new_position, new_direction



def parse_matrix(data) -> np.array:
    data_mapped = [[SYMBOLS[x] for x in line] for line in data.split('\n')]
    return np.array(data_mapped)


def find_shortest_path(matrix):
    # Find the starting point
    positions, directions = find_start_pipes(matrix)
    N = 1
    _continue = True
    while _continue:
        print(positions)
        for i in range(2):
            positions[i], directions[i] = iterate(matrix, positions[i], directions[i])
            # Check if any of the new positions lands on the other one
            # either the new first one on the old second one
            # or the new first one on the new second one
            if positions[0] == positions[1]:
                _continue = False
                break
        N += 1

    return N

def main():
    file = argv[1]
    with open(file) as f:
        data = f.read()
        matrix = parse_matrix(data)
        N = find_shortest_path(matrix)
        print(N)

if __name__ == '__main__':
    main()
        