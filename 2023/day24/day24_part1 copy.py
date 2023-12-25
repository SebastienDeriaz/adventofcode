from sys import argv


import numpy as np
import re

class Hailstone:
    def __init__(self, description : str) -> None:
        pattern = '(\d+), (\d+), (\d+) @ +(-?\d+), +(-?\d+), +(-?\d+)'
        m = re.match(pattern, description)
        values = [int(x) for x in m.groups()]
        self.p = np.block([[values[0]], [values[1]]])
        self.v = np.block([[values[3]], [values[4]]])

    def intersect(self, o):
        # unknowns are x, y, t
        A = np.block([
            [1, 0, -self.v[0,0], 0],
            [0, 1, -self.v[1,0], 0],
            [1, 0, 0, -o.v[0,0]],
            [0, 1, 0, -o.v[1, 0]]
        ])
        b = np.block([
            [self.p[0,0]],
            [self.p[1,0]],
            [o.p[0,0]],
            [o.p[1,0]]
        ])
        if np.linalg.det(A) == 0:
            # Singular matrix
            return None, None, None
        else:
            xyt = np.linalg.inv(A) @ b

            return xyt[:2,:], xyt[2, 0], xyt[3, 0] 


def parse_hailstones(data) -> list:
    hailstones = []
    for line in data.split('\n'):
        if line != '':
            hailstones.append(Hailstone(line))
    return hailstones

def count_intersections_in_test_area(hailstones : list, test_area : tuple):
    N = 0
    for ia, a in enumerate(hailstones):
        for b in hailstones[ia+1:]:
            p, t1, t2 = a.intersect(b)
            if p is not None:
                if t1 >= 0 and t2 >= 0 and test_area[0] <= p[0,0] <= test_area[1] and test_area[0] <= p[1,0] <= test_area[1]:
                    N += 1
    return N

def determine_rock(hailstones):
    # Take the first three
    A = np.block()


TEST_AREA = (200000000000000, 400000000000000)

def main():
    file = argv[1]
    with open(file) as f:
        data = f.read()
        hailstones = parse_hailstones(data)
        rock = determine_rock(hailstones)


        N = count_intersections_in_test_area(hailstones, TEST_AREA)
        print(N)

if __name__ == '__main__':
    main()
        