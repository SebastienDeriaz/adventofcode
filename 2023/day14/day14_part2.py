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
    tilted_platform[platform == SQUARE_ROCK] = SQUARE_ROCK

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

def spin_cycle(platform):
    N = 4
    for _ in range(4):
        platform = move_platform(platform)
        platform = np.rot90(platform, k=3)
    return platform

def platform_hash(platform : np.array):
    hash_input = ''.join([str(x) for x in platform.flat])

    return hash(hash_input)

def main():
    file = argv[1]
    with open(file) as f:
        data = f.read()
        platform = parse_platform(data)

        weights = []
        hashes = []

        N = 1_000_000_000

        for i in range(1, N+1):
            platform = spin_cycle(platform)
            hash = platform_hash(platform)
            weight = add_weights(platform)
            if hash in hashes:
                start = hashes.index(hash)+1
                cycle = [(j+start, w) for j, w in enumerate(weights[start-1:])]
                break
            hashes.append(hash)
            weights.append(weight)

        n_cycle_index = (N-cycle[0][0]) % len(cycle)
        print(cycle[n_cycle_index][1])

if __name__ == '__main__':
    main()