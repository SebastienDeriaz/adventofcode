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

        lines = [line for line in contents.split('\n') if line]
        
        total = 0
        operation = None
        local_total = None
        columns = list(zip(*lines))
        for characters in columns:
            if all(c == ' ' for c in characters):
                total += local_total
                #print(f' = {local_total}')
                local_total = None
                continue
            new_operation = characters[-1]
            if new_operation != ' ':
                operation = new_operation

            number = int(''.join(characters[:-1]))

            if local_total is None:
                local_total = number
                #print(number, end='')
            else:
                if operation == MULTIPLY:
                    local_total *= number
                    #print(f' * {number}', end='')
                elif operation == ADD:
                    local_total += number
                    #print(f' + {number}', end='')

        total += local_total
        #print()


                
    
    print(total)


    return


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