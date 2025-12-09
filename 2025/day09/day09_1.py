from sys import argv
import numpy as np

def main():
    file = argv[1]
    with open(file) as f:
        file_contents = f.read()

        positions = [[int(x) for x in line.split(',')] for line in file_contents.split('\n')]

        positions = np.array(positions)



    largest_area = 0
    for p in positions:
        areas = np.prod(np.abs(positions - p)+1, axis=1)
        #print(areas)
        largest_area = max(np.max(areas), largest_area)

    print(largest_area)




if __name__ == '__main__':
    main()