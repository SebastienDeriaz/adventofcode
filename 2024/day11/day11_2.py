import sys
from collections import Counter
import functools


@functools.cache
def n_stones_after_blink(stone, N):
    # Apply rules to that stone
    # If N > 1, apply rules to each successive one
    n = 0
    stones = []
    if stone == 0:
        stones.append(1)
    elif len(str(stone)) % 2 == 0:
        s_str = str(stone)
        left = int(s_str[:len(s_str)//2])
        right = int(s_str[len(s_str)//2:])
        stones.append(left)
        stones.append(right)
    else:
        stones.append(stone * 2024)
    if N > 1:
        for s in stones:
            n += n_stones_after_blink(s, N-1)
    else:
        n = len(stones)
    return n

def blink(stones, N):
    n = 0
    for s in stones:
        n += n_stones_after_blink(s, N)
    return n

def main():
    file = sys.argv[1]
    
    with open(file) as f:
        data = f.read()
        stones = [int(x) for x in data.split(' ')]

        N = 75
        print(blink(stones, N))

if __name__ == '__main__':
    main()