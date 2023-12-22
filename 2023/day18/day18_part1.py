from sys import argv
import re
from enum import Enum
import numpy as np


NORTH = 0
SOUTH = 1
WEST = 2
EAST = 3

DIRECTION_MAP = {
    'U' : NORTH,
    'D' : SOUTH,
    'L' : WEST,
    'R' : EAST
}


class Vec2D:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    def idx(self):
        return (self.y, self.x)

    def __add__(self, o):
        return Vec2D(self.x + o.x, self.y + o.y)

    def __sub__(self, o):
        return Vec2D(self.x - o.x, self.y - o.y)

    def move_in_direction(self, direction, N=1):
        if direction == NORTH:
            self.y -= N
        elif direction == SOUTH:
            self.y += N
        elif direction == EAST:
            self.x += N
        elif direction == WEST:
            self.x -= N
        else:
            raise ValueError(f"invalid directoin : {direction}")

    def __eq__(self, __o: object) -> bool:
        return self.x == __o.x and self.y == __o.y

    def __repr__(self) -> str:
        return f'({self.x},{self.y})'

    def rotate_90(self):
        return Vec2D(-self.y, self.x)

    def rotate_270(self):
        return Vec2D(self.y, -self.x)

def propagate(matrix, position, val):
    offsets = [
        Vec2D(0, 1),
        Vec2D(0, -1),
        Vec2D(1, 0),
        Vec2D(-1, 0)
    ]
    positions = [position]
    neighbors = []
    stop = False
    i = 0
    while not stop:
        stop = True
        for p in positions:
            matrix[p.idx()] = val
            i += 1
            for offset in offsets:
                new_position = p + offset
                if 0 <= new_position.x < matrix.shape[1] and 0 <= new_position.y < matrix.shape[0]:
                    if matrix[new_position.idx()] == 0:
                        if new_position not in neighbors:
                            neighbors.append(new_position)
                        stop = False
        positions = neighbors
        neighbors = []
    return i

def propagate_adjacent(matrix, position : Vec2D, direction : Vec2D):
    xy_rot = direction.rotate_90()
    on_the_left = position + xy_rot
    N = [0, 0]
    if 0 <= on_the_left.x < matrix.shape[1] and \
        0 <= on_the_left.y < matrix.shape[0] and \
                matrix[on_the_left.idx()] == 0:
        N[0] = propagate(matrix, on_the_left, 10)
    on_the_right = position - xy_rot
    if 0 <= on_the_right.x < matrix.shape[1] and \
        0 <= on_the_right.y < matrix.shape[0] and \
                matrix[on_the_right.idx()] == 0:
        N[1] = propagate(matrix, on_the_right, 20)
    return N

# From day 10
def count_enclosed(loop_matrix, loop):

    matrix = loop_matrix.copy()
    N = [0, 0]

    for p, next_p in zip(loop[:-1], loop[1:]):
        direction = next_p - p

        Nnew = propagate_adjacent(matrix, p, direction)
        N[0] += Nnew[0]
        N[1] += Nnew[1]

    return np.min(N)

def parse_dig_plan(data):
    instructions = []
    pattern = '(\w) (\d+) \(#(\w+)\)'
    for line in data.split('\n'):
        if line != '':
            groups = re.match(pattern, line).groups()
            instructions.append([
                DIRECTION_MAP[groups[0]],
                int(groups[1]),
                int(groups[2], 16)
            ])
    return instructions

def iterate_instructions(instructions):
    loop = [Vec2D(0,0)]
    for instruction in instructions:
        for _ in range(instruction[1]):
            new = Vec2D(loop[-1].x, loop[-1].y)
            new.move_in_direction(instruction[0])
            if new not in loop:
                loop.append(new)
    return loop

def generate_matrix(loop):
    instructions_matrix = np.array([[p.x, p.y] for p in loop])
    _min = np.min(instructions_matrix, axis=0)
    _max = np.max(instructions_matrix, axis=0)
    X = _min[0], _max[0]
    Y = _min[1], _max[1]
    M = np.zeros([Y[1]-Y[0]+1, X[1]-X[0]+1])

    for p in loop:
        M[p.idx()] = 1

    return M

def main():
    file = argv[1]
    with open(file) as f:
        data = f.read()
        instructions = parse_dig_plan(data)
        loop = iterate_instructions(instructions)
        loop_matrix = generate_matrix(loop)
        N = count_enclosed(loop_matrix, loop)
        total = N + np.sum(loop_matrix != 0)
        print(total)

if __name__ == '__main__':
    main()

        