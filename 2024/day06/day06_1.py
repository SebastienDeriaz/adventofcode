import sys
import numpy as np



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

VISITED = 'X'

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

def guard_positions(matrix):
    # Search the guard first
    for possible_guard_symbol, direction in GUARD_DIRECTIONS.items():
        rp, cp = np.where(matrix == possible_guard_symbol)
        if len(rp) > 0 and len(cp) > 0:
            p = np.array([rp[0], cp[0]])
            d = direction
            break

    visit_counter = 0
    while True:
        # Visit that location
        if matrix[tuple(p)] != VISITED: 
            matrix[tuple(p)] = VISITED
            visit_counter += 1
        n_p = p + d
        # See if the next position is valid or not
        if 0 <= n_p[0] < matrix.shape[0] and 0 <= n_p[1] < matrix.shape[1]:
            # Valid
            # See if there's an obstacle up ahead
            while matrix[tuple(n_p)] == OBSTACLE:
                d = turn_clockwise(d)
                n_p = p + d
            # Go forward
            p = n_p
        else:
            # Outside, break out of the loop
            break

    return visit_counter
        
        

def main():
    file = sys.argv[1]

    with open(file) as f:
        data = f.read()

        matrix = parse_matrix(data)

        N = guard_positions(matrix)

        print(N)



if __name__ == '__main__':
    main()