import sys
import numpy as np

UP = np.array([1, 0])
DOWN = np.array([-1, 0])
RIGHT = np.array([0, 1])
LEFT = np.array([0, -1])

DIRECTIONS = [UP, DOWN, LEFT, RIGHT]

WALL = '#'
START = 'S'
END = 'E'
VISITED = 'x'
EMPTY = '.'

TURN_COST = 1000
FORWARD_COST = 1


def valid(matrix, p):
    return 0 <= p[0] < matrix.shape[0] and 0 <= p[1] < matrix.shape[1]

def print_matrix(matrix):
    for line in matrix:
        print(''.join(line))
    

def deer(matrix, start, direction, cost=0):
    print(f'Deer at {start}')
    if matrix[tuple(start)] == END:
        # End here
        output = cost
    else:
        while True:
            free_directions = []
            for d in DIRECTIONS:
                cell = matrix[tuple(start+d)]
                if cell == EMPTY or cell == END:
                    free_directions.append(d)
            
            print(f'')
            if len(free_directions) == 0:
                # Stuck
                return [None]
            elif len(free_directions) == 1:
                # Go in that direction
                if np.array_equal(d, direction):
                    cost += FORWARD_COST
                else:
                    cost += TURN_COST
                direction = d
                start += direction
                matrix[tuple(start)] = VISITED
                print_matrix(matrix)
                input()
            else:
                # Too many possibilities, evaporate this deer
                # and spawn new ones
                deer_scores = []
                for d in free_directions:
                    if np.array_equal(d, direction):
                        new_cost = FORWARD_COST
                    else: 
                        new_cost = TURN_COST
                    deer_scores.append(deer(matrix, start+d, d, new_cost))
                output = min(deer_scores)
                break

    return output



        

    






def parse_file(file):
    with open(file) as f:
        data = f.read()
        values = [list(line) for line in data.split('\n')]
        return np.array(values)


def main():
    matrix = parse_file(sys.argv[1])

    print_matrix(matrix)


    # Find the start point
    start = np.array(np.where(matrix == START)).squeeze()

    deer(matrix.copy(), start, RIGHT)


if __name__ == '__main__':
    main()