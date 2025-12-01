"""
Day01 - Part 2
"""
from sys import argv
from math import floor

# 2399 too low
# 6472 too high
# 6239 too low
# 6363 wrong
# 6358 wrong
# 6408 wrong
# 6189 wrong
# 6305 good !

MAX = 99

def next_value(x : int, movement : int):

    value = x + movement

    turns = floor(value / (MAX + 1))

    zero_count = abs(turns)

    if turns < 0 and x == 0:
        zero_count -= 1

    value = value % (MAX + 1)

    if turns > 0 and value == 0:
        zero_count -= 1

    if value == 0:
        zero_count += 1

    #print(f'{x:<4} {+movement:4} -> {value:4} ({zero_count:+d})')
    
    return value, zero_count

def main():
    value = 50
    file = argv[1]
    zero_counter = 0

    with open(file, 'r') as f:
        contents = f.read()

        for line in contents.split('\n'):
            if not line:
                continue
            
            if line.startswith('L'):
                movement = -int(line[1:])
            else:
                movement = int(line[1:])

            value, counter = next_value(value, movement)

            zero_counter += counter

    print(zero_counter)


if __name__ == '__main__':
    main()