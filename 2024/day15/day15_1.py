import sys
import numpy as np

WALL = '#'
BOX = 'O'
ROBOT = '@'
EMPTY = '.'

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

def parse_data(data : str):
    matrix = []
    moves = []
    parsing_map = True

    for line in data.split('\n'):
        if not line.startswith(WALL):
            parsing_map = False
        
        if parsing_map:
            matrix.append(list(line.strip('\n')))
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
    R, C = np.where(matrix == BOX)
    for r, c in zip(R, C):
        gps_value += r * 100 + c

    return gps_value

def move_robot_and_boxes(matrix, moves):
    matrix = matrix.copy()
    # Find the robot position
    R, C = np.where(matrix == ROBOT)
    robot = np.array([R[0], C[0]])

    def valid(p):
        return 0 <= p[0] < matrix.shape[0] and 0 <= p[1] < matrix.shape[1]

    for m in moves:
        # Look in that direction
        # If there's a wall, stop
        # If there's a box, look further
        #   If there's a hole, move the boxes
        #   If there's a wall, stop
        k = 1
        while True:
            p2 = robot + k * m
            if valid(p2):
                if matrix[tuple(p2)] == EMPTY:
                    # Ok to move the robot (and boxes)
                    for i in range(k-1):
                        # Move each box (if any)
                        new_pos = p2 - i * m
                        previous_pos = p2 - (i+1) * m
                        matrix[tuple(new_pos)] = matrix[tuple(previous_pos)]
                    matrix[tuple(robot)] = EMPTY
                    robot += m
                    matrix[tuple(robot)] = ROBOT
                    break
                elif matrix[tuple(p2)] == WALL:
                    # Do not do anything but stop here
                    break
                elif matrix[tuple(p2)] == BOX:
                    # Continue the loop
                    pass
            else:
                # There's a hole somehow ??
                raise ValueError('Iterator got out of the map')
            k += 1
        

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