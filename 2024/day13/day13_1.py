import numpy as np
import sys
import re
import z3

COST = {
    'A' : 3,
    'B' : 1
}

MAX_PRESSES = 100


def parse_data(data):
    PATTERN = "Button A: X([\+\-\d]+), Y([\+\-\d]+)\nButton B: X([\+\-\d]+), Y([\+\-\d]+)\nPrize: X=([\+\-\d]+), Y=([\+\-\d]+)"

    machines = []
    for values in re.findall(PATTERN, data):
        machines.append([int(x) for x in values])

    return machines


def solve(machines):

    # Turns out using linear algebra doesn't work because the values have to be integer
    # z3 is used instead... meh

    costs = []

    for ax, ay, bx, by, px, py in machines:
        pa, pb = z3.Ints('pa pb')
        s = z3.Solver()
        
        s.add(pa * ax + pb * bx == px, pa * ay + pb * by == py, pa >= 0, pa <= MAX_PRESSES, pb >= 0, pb <= MAX_PRESSES)
        s.check()
        try:
            model = s.model()
        except z3.z3types.Z3Exception:
            cost = None
        else:
            cost = model[pa].as_long() * COST['A'] + model[pb].as_long() * COST['B']

        costs.append(cost)
        
    return costs

def main():
    file = sys.argv[1]

    with open(file) as f:
        data = f.read()

        machines = parse_data(data)

        costs = solve(machines)

        print(sum(filter(None, costs)))



if __name__ == '__main__':
    main()