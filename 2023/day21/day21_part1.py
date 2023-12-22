# Create a matrix
# Fill it with rocks and ground
# Iterate by filling all positions adjacent to a 'O'

from sys import argv
import numpy as np


GARDEN_PLOT = 0
ROCK = 1
REACHED_TILE = 2
STARTING_POSITION = 3

SYMBOL_MAP = {
    '.' : GARDEN_PLOT,
    '#' : ROCK,
    'S' : STARTING_POSITION
}


def parse_matrix(data):
    return np.array([[SYMBOL_MAP[x] for x in line] for line in data.split('\n') if line != ''])


def set_free_adjacent(matrix, position, value):
    neighbors = [
        (-1, 0),
        (1, 0),
        (0, 1),
        (0, -1)
    ]

    for y, x in neighbors:
        p = position[1]+y, position[0]+x
        if 0 <= p[0] < matrix.shape[1] and 0 <= p[1] < matrix.shape[0] and matrix[p] == GARDEN_PLOT:
            matrix[p] = value


def iterate(matrix):
    outputs = np.zeros_like(matrix)
    outputs[matrix == ROCK] = ROCK

    
    
    for y, x in zip(*np.where(matrix >= REACHED_TILE)):
        set_free_adjacent(outputs, (x,y), REACHED_TILE)

    return outputs



N_STEPS = 64

def main():
    file = argv[1]
    with open(file) as f:
        matrix = parse_matrix(f.read())

        for _ in range(N_STEPS):
            matrix = iterate(matrix)

        print(np.sum(matrix == REACHED_TILE))


if __name__ == '__main__':
    main()
