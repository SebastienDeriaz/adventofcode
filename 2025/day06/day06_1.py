from sys import argv
import numpy as np

MULTIPLY = '*'
ADD = '+'

def main():
    file = argv[1]


    number_lines = []
    operations = []
    with open(file) as f:
        contents = f.read()

        for line in contents.split('\n'):
            if line[0].isdigit() or line[0] == ' ':
                number_lines.append([int(x) for x in line.split(' ') if x])
            else:
                operations = [x for x in line.split(' ') if x]


    numbers_matrix = np.array(number_lines)

    # print(numbers_matrix)
    # print(operations)

    total = 0
    for op, numbers in zip(operations, numbers_matrix.T):
        if op == MULTIPLY:
            total += np.prod(numbers)
        elif op == ADD:
            total += np.sum(numbers)
        else:
            raise ValueError
        
    print(total)






if __name__ == '__main__':
    main()