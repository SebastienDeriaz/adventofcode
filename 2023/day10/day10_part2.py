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

def position_add(x1, x2):
    return x1[0] + x2[0], x1[1] + x2[1]

def position_substract(x1, x2):
    return x1[0] - x2[0], x1[1] - x2[1]


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

def propagate(matrix, position, val):
    offsets = [
        (0, 1),
        (0, -1),
        (1, 0),
        (-1, 0)
    ]
    i = 1
    print(f'propagate {val} to {position}')
    matrix[position[::-1]] = val
    for offset in offsets:
        new_position = position_add(position, offset)
        if 0 <= new_position[0] < matrix.shape[1] and 0 <= new_position[1] < matrix.shape[0]:
            if matrix[new_position[::-1]] == GROUND:
                i += propagate(matrix, new_position, val)

    return i

def count_enclosed(matrix):
    # Find the starting point
    positions, directions = find_start_pipes(matrix)
    position = positions[0]
    direction = directions[0]
    N = [0, 0]
    _continue = True
    right_counter = 0
    left_counter = 0
    while _continue:
        if direction & LEFT:
            left_counter += 1
        elif direction & RIGHT:
            right_counter += 1

        if direction in [NORTH, SOUTH]:
            xy = DIRECTION_TO_XY[direction]
            on_the_left = position_substract(position, xy[::-1])
            if 0 <= on_the_left[0] < matrix.shape[1] and matrix[on_the_left[::-1]] == GROUND:
                N[0] += propagate(matrix, on_the_left, LEFT)
            on_the_right = position_add(position, xy[::-1])
            if 0 <= on_the_right[0] < matrix.shape[1] and matrix[on_the_right[::-1]] == GROUND:
                N[1] += propagate(matrix, on_the_right, RIGHT)

        position, direction = iterate(matrix, position, direction)
        # Add each point on the right

        if direction == 0:
            # Reached the end
            break
    print(f'left : {left_counter}, right : {right_counter}')
    plt.imshow(matrix)
    plt.colorbar()
    plt.show()
    return N

def main():
    file = argv[1]
    with open(file) as f:
        data = f.read()
        matrix = parse_matrix(data)
        N = count_enclosed(matrix)
        print(N)

if __name__ == '__main__':
    main()
        