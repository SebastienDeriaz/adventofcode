import sys
import numpy as np

START = 0
END = 9

UP = np.array([-1, 0])
DOWN = np.array([1, 0])
RIGHT = np.array([0, 1])
LEFT = np.array([0, -1])

DIRECTIONS = [UP, DOWN, LEFT, RIGHT]

def parse_data(data):
    return np.array([[int(x) for x in line] for line in data.split('\n')])


def iterate_path(matrix, start, k=0) -> list:
    paths = []
    for d in DIRECTIONS:
        p = start + d
        if 0 <= p[0] < matrix.shape[0] and 0 <= p[1] < matrix.shape[1]: 
            if matrix[tuple(p)] == matrix[tuple(start)] + 1:
                # Found a way
                if matrix[tuple(p)] == END:
                    # Stop here
                    paths.append(np.stack([start, p], axis=0))
                else:
                    for path in iterate_path(matrix, p, k+1):
                        paths.append(np.concatenate([start.reshape(1,-1), path], axis=0))
    return paths

def find_paths(matrix):
    paths = []
    # Loop over starting points
    R, C = np.where(matrix == START)
    for s in zip(R, C):
        s = np.array(s)
        paths += iterate_path(matrix, s)
    
    return paths


def display_path(matrix, path):
    dot_matrix = np.ones_like(matrix) * -1
    for p in path:
        dot_matrix[tuple(p)] = matrix[tuple(p)]
    
    string = ''
    for row in dot_matrix:
        for x in row:
            if x < 0:
                string += '.'
            else:
                string += str(x)
        string += '\n'
    
    print(string)

def main():
    file = sys.argv[1]

    with open(file) as f:
        data = f.read()

        matrix = parse_data(data)

        paths = find_paths(matrix)
            
        print(len(paths))

        

if __name__ == '__main__':
    main()