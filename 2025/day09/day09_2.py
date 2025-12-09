from sys import argv
import numpy as np

def main():
    file = argv[1]
    with open(file) as f:
        file_contents = f.read()

        positions = [[int(x) for x in line.split(',')] for line in file_contents.split('\n')]

        positions = np.array(positions)


    rectangles = [] # a, b, area

    for i, a in enumerate(positions):
        for j, b in enumerate(positions):
            if j <= i:
                continue
            area = np.prod(np.abs(a-b)+1)
            if area > 0:
                rectangles.append((a, b, area))

    rectangles.sort(key=lambda x : x[2], reverse=True)

    #print(rectangles)

    for a, b, area in rectangles:
        c = np.array([a[0], b[1]])
        d = np.array([b[0], a[1]])

        print(a, b, c, d)
        # Check if c and d are inside the green area
        
        







        # Scalar product between all the other vectors and a+b ?




if __name__ == '__main__':
    main()