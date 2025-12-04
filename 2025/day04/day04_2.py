from sys import argv
import numpy as np
from scipy.ndimage import correlate

def main():
    file = argv[1]

    lines = []
    with open(file) as f:
        data = f.read()

        for line in data.split('\n'):
            if line:
                lines.append([1 if x == '@' else 0 for x in line])

    matrix = np.array(lines)

    kernel = np.block([
        [1, 1, 1],
        [1, 0, 1],
        [1, 1, 1]
    ])


    removed = 0
    while True:

        output = correlate(matrix, kernel, mode='constant', cval=0)


        to_remove = np.logical_and(matrix > 0, output < 4).astype(int)
        removable = np.sum(to_remove)
        if removable == 0:
            break
        removed += removable
        matrix -= to_remove

    print(removed)

if __name__ == '__main__':
    main()