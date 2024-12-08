import numpy as np
import sys

EMPTY = '.'

def place_antinodes(matrix):
    antinodes = np.zeros_like(matrix, dtype=int)
    
    for antenna in np.unique(matrix):
        if antenna != EMPTY:
            R, C = np.where(matrix == antenna)
            for r1, c1 in zip(R, C):
                v1 = np.array([r1, c1])
                for r2, c2 in zip(R, C):
                    v2 = np.array([r2, c2])
                    if not np.array_equal(v1, v2):
                        dist_vector = v1 - v2
                        d = 0
                        antinodes[tuple(v1)] = 1 # The antenna is an antinode
                        while True:
                            d += dist_vector
                            valid = False
                            for ds in [+d, -d]:
                                p = v1 + ds
                                if 0 <= p[0] < antinodes.shape[0] and 0 <= p[1] < antinodes.shape[1]:
                                    antinodes[tuple(p)] = 1
                                    valid = True
                            if not valid:
                                break

    return antinodes




def parse_matrix(file):
    with open(file) as f:
        data = f.read()
        matrix = np.array([list(x) for x in data.split('\n')])

    return matrix



def main():
    file = sys.argv[1]

    matrix = parse_matrix(file)

    antinodes = place_antinodes(matrix)
    
    print(np.sum(antinodes))

if __name__ == '__main__':
    main()