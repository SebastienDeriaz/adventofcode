from sys import argv
from day01_02 import next_value
MAX = 99



def main():
    x = int(argv[1])
    movement_string = argv[2]
    if movement_string.startswith('L'):
        movement = -int(movement_string[1:])
    else:
        movement = int(movement_string[1:])

    print(x, movement)
    value, zero_count = next_value(x, movement)
    
    print(f'{x}+{movement_string} = {value:d} {zero_count:+d}')



if __name__ == '__main__':
    main()
