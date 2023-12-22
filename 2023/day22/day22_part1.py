# Bricks are stacked "magically" (like minecraft)
# Maybe the bricks don't need to be "settled"
# Each brick could have a bit field of folded X-Y positions
# A brick is above another if it shares a X-Y bit field and if one of its z coordinates is higher
from sys import argv
import re
from itertools import product

def interleave_bits(x, y):
    result = 0
    bit_position = 0
    while x > 0 or y > 0:
        result |= ((x & 1) << (2 * bit_position)) | ((y & 1) << (2 * bit_position + 1))
        x >>= 1
        y >>= 1
        bit_position += 1
    return result

class Brick:
    def __init__(self, str_description : str) -> None:
        pattern = '(\d+),(\d+),(\d+)~(\d+),(\d+),(\d+)'
        m = re.match(pattern, str_description)

        self.x1 = int(m.group(1))
        self.y1 = int(m.group(2))
        self.z1 = int(m.group(3))
        self.x2 = int(m.group(4))
        self.y2 = int(m.group(5))
        self.z2 = int(m.group(6))

    def __repr__(self) -> str:
        return f'({self.x1},{self.y1},{self.z1})~({self.x2},{self.y2},{self.z2})'

    def __lt__(self, b):
        return self.z2 < b.z1
    
    def __gt__(self, b):
        return self.z1 > b.z2

    def mask(self, z):
        if self.z1 <= z <= self.z2:
            mask = sum([1 << interleave_bits(x, y) for x in range(self.x1, self.x2+1) for y in range(self.y1, self.y2+1)])
        else:
            mask = 0
        return mask

    # & operator (X-Y)
    # <, > operators (height)

def parse_bricks(data) -> list:
    bricks = []
    for line in data.split('\n'):
        if line != '':
            bricks.append(Brick(line))

    return bricks

def count_safe(bricks : list):
    free = [True for _ in range(len(bricks))]
    for bi1, b1 in enumerate(bricks):
        for bi2, b2 in enumerate(bricks):
            if bi2 == bi1:
                continue
            if b1 & b2 and b1 < b2:
                # B1 is below B2
                print(f'Removing {b1} (below {b2})')
                free[bi1] = False
                break

    return sum(free)

def simulate_bricks_fall(bricks : list):
    mask = 0
    z = 1
    bricks_to_move = bricks.copy()
    while True:
        for b in bricks:
            
        



        z += 1


def main():
    file = argv[1]
    with open(file) as f:
        data = f.read()
        bricks = parse_bricks(data)
        bricks_down = simulate_bricks_fall(bricks)
        for b in bricks:
            print(f'{b} : {b.mask():020b}')
        print(count_safe(bricks))

if __name__ == '__main__':
    main()

