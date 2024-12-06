import sys
import numpy as np
from time import sleep
from tqdm import tqdm



RIGHT = np.array([0, 1])
LEFT = np.array([0, -1])
UP = np.array([-1, 0])
DOWN = np.array([1, 0])

GUARD_DIRECTIONS = {
    '>' : RIGHT,
    '<' : LEFT,
    '^' : UP,
    'v' : DOWN
}

OBSTACLE = '#'
NEW_OBSTACLE = 'O'

VISITED = {
    tuple(RIGHT) : '-',
    tuple(LEFT) : '_',
    tuple(UP) : '|',
    tuple(DOWN) : '/',   
}

VISITED_COMMON = 'X'

EMPTY = '.'


def turn_clockwise(direction):
    # RIGHT -> DOWN
    # DOWN -> LEFT
    # LEFT -> UP
    # UP -> RIGHT
    return np.array([direction[1], -direction[0]])

def parse_matrix(data):
    matrix = np.array([list(line) for line in data.split('\n')])
    return matrix

def loops(matrix):
    matrix = matrix.copy()
    # Search the guard first
    for possible_guard_symbol, direction in GUARD_DIRECTIONS.items():
        rp, cp = np.where(matrix == possible_guard_symbol)
        if len(rp) > 0 and len(cp) > 0:
            start = np.array([rp[0], cp[0]])
            d = direction
            break

    loops = False
    p = start
    while True:
        # Visit that location
        if matrix[tuple(p)] == VISITED[tuple(d)]:
            # If we're back on our tracks, break out of the loop
            loops = True
            break
        if matrix[tuple(p)] not in list(VISITED.values()): 
            matrix[tuple(p)] = VISITED[tuple(d)]
        n_p = p + d
        # See if the next position is valid or not
        if 0 <= n_p[0] < matrix.shape[0] and 0 <= n_p[1] < matrix.shape[1]:
            # Valid
            # See if there's an obstacle up ahead
            while matrix[tuple(n_p)] in [OBSTACLE, NEW_OBSTACLE]:
                d = turn_clockwise(d)
                n_p = p + d
            # Go forward
            p = n_p
        else:
            # Outside, break out of the loop
            break

    return loops, matrix, start
        
        

def main():
    file = sys.argv[1]

    with open(file) as f:
        data = f.read()

        matrix = parse_matrix(data)
        

        initial_loops, visited_matrix, start = loops(matrix)
        
        # Replace every visited character with a single common one
        for c in VISITED.values():
            visited_matrix[visited_matrix == c] = VISITED_COMMON

        R, C = np.where(visited_matrix == VISITED_COMMON)
        coordinates = [np.array([r, c]) for r, c in zip(R, C)]
        loop_counter = int(initial_loops)
        for p in tqdm(coordinates):
            if np.array_equal(p, start):
                continue
            new_matrix = matrix.copy()
            new_matrix[tuple(p)] = NEW_OBSTACLE
            l, _, _ = loops(new_matrix)
            if l:
                loop_counter += 1

        

        print(loop_counter)



if __name__ == '__main__':
    main()