import sys
import numpy as np
from time import sleep

WALL = '#'
BOX_INPUT = 'O'
BOX_LEFT = '['
BOX_RIGHT = ']'
ROBOT = '@'
EMPTY = '.'

DISPLAY = True

UP = np.array([-1, 0])
DOWN = np.array([1, 0])
RIGHT = np.array([0, 1])
LEFT = np.array([0, -1])

DIRECTION_CHARACTERS = {
    '^' : UP,
    'v' : DOWN,
    '>' : RIGHT,
    '<' : LEFT
}

def scale_line(line):
    MAP = {
        '#' : '##',
        'O' : '[]',
        '@' : '@.',
        '.' : '..'
    }

    return list(''.join([MAP[x] for x in line]))

def parse_data(data : str):
    matrix = []
    moves = []
    parsing_map = True

    for line in data.split('\n'):
        if not line.startswith(WALL):
            parsing_map = False
        
        if parsing_map:
            matrix.append(scale_line(line.strip('\n')))
        else:
            moves += [DIRECTION_CHARACTERS[x] for x in line if x != '\n']

        
    return np.array(matrix), moves


def print_map(matrix):
    for row in matrix:
        for c in row:
            print(c, end='')
        print()


def gps(matrix):
    gps_value = 0
    R, C = np.where(matrix == BOX_LEFT)
    for r, c in zip(R, C):
        gps_value += r * 100 + c

    return gps_value

def valid(matrix, p):
    return 0 <= p[0] < matrix.shape[0] and 0 <= p[1] < matrix.shape[1]


def is_vertical(d):
    return d[0] != 0

def add_not_existing(l : list, elements : list):
    for e in elements:
        for li in l:
            if np.array_equal(li, e):
                break
        else:
            l.append(e)

def recursive_find_boxes(matrix, p, d):
    p2 = p + d
    output = []

    if not valid(matrix, p2):
        raise ValueError('Iterator got out')

    #print(f'Look at {p2}...', end='')
    # If there's a wall, stop everything
    if matrix[tuple(p2)] != WALL:
        #print(f'-{matrix[tuple(p2)]}-')
        if is_vertical(d) and matrix[tuple(p2)] != EMPTY:
            # If it is vertical and there's a box above, we might need to check more boxes
            output = [p2]
            if matrix[tuple(p2)] == BOX_LEFT:
                _next = [p2, p2+RIGHT]
            else:
                _next = [p2, p2+LEFT]
            for n in _next:
                new_boxes = recursive_find_boxes(matrix, n, d)
                if new_boxes is None:
                    # Blocked
                    output = None
                    break
                else:
                    add_not_existing(output, new_boxes)
        else:
            # If it is horizontal, it's easy
            if matrix[tuple(p2)] == EMPTY:
                # Return the set
                output = [p2]
            else:
                new_boxes = recursive_find_boxes(matrix, p2, d)
                if new_boxes is None:
                    output = None
                else:
                    output = [p2]
                    add_not_existing(output, new_boxes)
    else:
        #print(f'Wall')
        output = None
    # Remove duplicates
    #print(f' -> {output}')
    return output

def move_robot_and_boxes(matrix, moves):
    matrix = matrix.copy()
    # Find the robot position
    R, C = np.where(matrix == ROBOT)
    robot = np.array([R[0], C[0]])

    for m in moves:
        output = recursive_find_boxes(matrix, robot, m)
        #print(f'{output=}')
        if output is not None:
            # Move everything by one
            # Reorder the positions
            output.sort(key=lambda x : np.sum(x * m))
            for c in output[::-1]:
                matrix[tuple(c)] = matrix[tuple(c-m)]
                matrix[tuple(c-m)] = EMPTY
            robot += m

        if DISPLAY:
            print_map(matrix)
            sleep(0.1)
        
    return matrix



def main():
    file = sys.argv[1]
    with open(file) as f:
        data = f.read()

        matrix, moves = parse_data(data)
        
        map = move_robot_and_boxes(matrix, moves)

        print(gps(map))


if __name__ == '__main__':
    main()