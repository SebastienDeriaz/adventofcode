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

MAX = 99

def next_value(x : int, movement : int):

    previous_value = x

    value = x + movement

    counts = 0
    i = 0
    while True:
        if value > MAX:
            value -= MAX+1
            if previous_value != 0:
                counts += 1
        elif value < 0:
            value += MAX+1
            if previous_value != 0:
                counts += 1
        else:
            if value == 0 and i != 0:
                counts += 1
            break
    
        previous_value = value

        i += 1

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

            previous_value = value
            value += movement  

            
           

            # if previous_value == 0 and movement < 0:
            #     counts -= 1

            # if value == 0:
            #     if counts == 0:
            #         counts += 1

                
            print(f'{line:<4} {previous_value:4} -> {value:4}', end='')
            
            print(f' +{counts}')
            zero_counter += counts
    

    print(zero_counter)


if __name__ == '__main__':
    main()