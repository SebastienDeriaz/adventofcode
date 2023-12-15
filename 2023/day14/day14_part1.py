from sys import argv
import numpy as np

ROUND_ROCK = 2
SQUARE_ROCK = 1
GROUND = 0
SYMBOLS = {
    'O' : ROUND_ROCK,
    '#' : SQUARE_ROCK,
    '.' : GROUND
}

def parse_platform(data):
    return np.array([[SYMBOLS[x] for x in line] for line in data.split('\n') if line != ''])

def move_platform(platform):
    
    tilted_platform = np.zeros_like(platform)

    for column in range(platform.shape[1]):
        square_rocks_positions = np.where(platform[:, column] == SQUARE_ROCK)[0]

        for i in range(-1, square_rocks_positions.size):
            if i == -1:
                current_square = -1
            else:
                current_square = square_rocks_positions[i]
            if i == len(square_rocks_positions)-1:
                # Last one
                next_square = None
            else:
                next_square = square_rocks_positions[i+1]

            # Take all of the rocks from the current one + 1 up to the next one
            rocks_to_move = int(np.sum(platform[current_square+1:next_square, column] == ROUND_ROCK))
            tilted_platform[current_square+1:current_square+1+rocks_to_move, column] = ROUND_ROCK

    return tilted_platform

def add_weights(platform):
    weight_matrix = (np.arange(platform.shape[0], dtype=int)+1)[::-1].reshape(-1, 1) @ np.ones(platform.shape[1], dtype=int).reshape(1, -1)

    weights = (platform == ROUND_ROCK) * weight_matrix

    return np.sum(weights)


def main():
    file = argv[1]
    with open(file) as f:
        data = f.read()
        platform = parse_platform(data)
        tilted_platform = move_platform(platform)
        total = add_weights(tilted_platform)
        print(total)

if __name__ == '__main__':
    main()