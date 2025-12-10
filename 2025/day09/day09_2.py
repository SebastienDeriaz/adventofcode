from sys import argv
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

# 875049660 too low

def main():
    file = argv[1]
    with open(file) as f:
        file_contents = f.read()

        positions = [[int(x) for x in line.split(',')] for line in file_contents.split('\n')]

        positions = np.array(positions)

    # Record all of the rectangles
    rectangles = [] # a, c, area

    for i, a in enumerate(positions):
        for j, c in enumerate(positions):
            if j <= i:
                continue
            area = np.prod(np.abs(a-c)+1)
            if area > 0:
                rectangles.append((a, c, area))

    rectangles.sort(key=lambda x : x[2], reverse=True)

    # Remove all of the ones who have lines going through them
    for a, c, area in tqdm(rectangles):
        valid = True

        for p1, p2 in zip(positions, np.roll(positions, -1, axis=0)):
            
            # eewww but it works, basically check if the line intersects the rectangle
            if p1[0] == p2[0]:
                # Vertical
                lmin_a = np.min([p1[1], p2[1]])
                lmax_a = np.max([p1[1], p2[1]])
                rmin_a = np.min([a[1], c[1]])
                rmax_a = np.max([a[1], c[1]])

                rmin_b = np.min([a[0], c[0]])
                rmax_b = np.max([a[0], c[0]])
                l_b = p1[0]

            elif p1[1] == p2[1]:
                # Horizontal
                lmin_a = np.min([p1[0], p2[0]])
                lmax_a = np.max([p1[0], p2[0]])
                rmin_a = np.min([a[0], c[0]])
                rmax_a = np.max([a[0], c[0]])

                rmin_b = np.min([a[1], c[1]])
                rmax_b = np.max([a[1], c[1]])
                l_b = p1[1]
            else:
                raise RuntimeError(f'Unknown line {p1}->{p2}')
            
            cross = lmax_a > rmin_a and lmin_a < rmax_a and rmin_b < l_b < rmax_b

            if cross:
                valid = False
                break
        
        if valid:
            print(area)
            break

if __name__ == '__main__':
    main()