"""
Day01 - Part 1
"""
from sys import argv

def main():
    value = 50
    file = argv[1]

    movements = []

    with open(file, 'r') as f:
        contents = f.read()

        for line in contents.split('\n'):
            if not line:
                continue
            
            if line.startswith('L'):
                movement = -int(line[1:])
            else:
                movement = int(line[1:])

            movements.append(movement)
    
    zero_counter = 0
    for movement in movements:
        value += movement
        value %= 100
        if value == 0:
            zero_counter += 1

    print(zero_counter)



if __name__ == '__main__':
    main()