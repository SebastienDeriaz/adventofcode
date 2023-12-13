from sys import argv
import numpy as np
from enum import Enum
import matplotlib.pyplot as plt


NORTH = (1 << 0) # 1
SOUTH = (1 << 1) # 2
EAST =  (1 << 2) # 4
WEST =  (1 << 3) # 8
GROUND = -1
STARTING_POSITION = 0
LEFT = (1 << 4)
RIGHT = (1 << 5)

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

def propagate(matrix, position, val):
    offsets = [
        (0, 1),
        (0, -1),
        (1, 0),
        (-1, 0)
    ]
    positions = [position]
    neighbors = []
    stop = False
    i = 0
    while not stop:
        stop = True
        for p in positions:
            matrix[p[::-1]] = val
            i += 1
            for offset in offsets:
                new_position = position_add(p, offset)
                if 0 <= new_position[0] < matrix.shape[1] and 0 <= new_position[1] < matrix.shape[0]:
                    if matrix[new_position[::-1]] == GROUND:
                        if new_position not in neighbors:
                            neighbors.append(new_position)
                        stop = False
        positions = neighbors
        neighbors = []
    return i


def position_add(x1, x2):
    return x1[0] + x2[0], x1[1] + x2[1]

def position_substract(x1, x2):
    return x1[0] - x2[0], x1[1] - x2[1]

def position_rotation_clockwise(x):
    return x[1], -x[0]

def position_rotation_counterclockwise(x):
    return -x[1], x[0]


def find_start_pipes(matrix):
    # Find the start
    yx = np.array(np.where(matrix == STARTING_POSITION))
    # Find the start pipes
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
    start = (yx[1,0], yx[0,0])
    return start, positions, directions

def iterate(matrix, position, direction):
    d = DIRECTION_TO_XY[direction]
    input_direction = XY_TO_DIRECTION[tuple(-x for x in d)]
    new_position = (position[0] + d[0], position[1] + d[1])
    new_direction = matrix[new_position[::-1]] & (~input_direction)
    return new_position, new_direction



def parse_matrix(data) -> np.array:
    data_mapped = [[SYMBOLS[x] for x in line] for line in data.split('\n')]
    return np.array(data_mapped)

def find_loop(matrix):
    # Find the starting point
    start, positions, directions = find_start_pipes(matrix)
    N = 1
    loop = np.zeros_like(matrix)
    direction = directions[0]
    position = positions[0]
    _continue = True
    loop[start[::-1]] = 1
    while _continue:
        loop[position[::-1]] = 1
        position, direction = iterate(matrix, position, direction)
        if direction == 0:
            _continue = False
            loop[position[::-1]] = 1

    return loop

def propagate_adjacent(matrix, position, direction):
    xy = DIRECTION_TO_XY[direction]
    xy_rot = position_rotation_counterclockwise(xy)
    on_the_left = position_add(position, xy_rot)
    N = [0, 0]
    if 0 <= on_the_left[0] < matrix.shape[1] and \
        0 <= on_the_left[1] < matrix.shape[0] and \
                matrix[on_the_left[::-1]] == GROUND:
        N[0] = propagate(matrix, on_the_left, LEFT)
    on_the_right = position_substract(position, xy_rot)
    if 0 <= on_the_right[0] < matrix.shape[1] and \
        0 <= on_the_right[1] < matrix.shape[0] and \
                matrix[on_the_right[::-1]] == GROUND:
        N[1] = propagate(matrix, on_the_right, RIGHT)
    return N

def count_enclosed(matrix, loop):
    filtered_matrix = matrix.copy()
    filtered_matrix[loop == 0] = GROUND
    # Find the starting point
    _, positions, directions = find_start_pipes(filtered_matrix)
    N = [0, 0]
    direction = directions[0]
    position = positions[0]
    _continue = True
    while _continue:
        Nnew = propagate_adjacent(filtered_matrix, position, direction)        
        N[0] += Nnew[0]
        N[1] += Nnew[1]

        old_direction = direction
        position, direction = iterate(filtered_matrix, position, direction)

        Nnew = propagate_adjacent(filtered_matrix, position, old_direction)
        N[0] += Nnew[0]
        N[1] += Nnew[1]
        
        if direction == 0:
            _continue = False
    return N

def main():
    file = argv[1]
    with open(file) as f:
        data = f.read()
        matrix = parse_matrix(data)
        loop = find_loop(matrix)
        N = count_enclosed(matrix, loop)
        print(N)

if __name__ == '__main__':
    main()
        