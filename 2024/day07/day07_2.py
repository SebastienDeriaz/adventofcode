import sys
import re
from itertools import product
from primefac import primefac
from enum import Enum
from tqdm import tqdm

def parse_file(data):
    PATTERN = '(\d+):([\d+ ]+)'
    equations = []
    for line in data.split('\n'):
        value, numbers = re.match(PATTERN, line).groups()
        equations.append((int(value), [int(x) for x in filter(None, numbers.split(' '))]))

    return equations

class Operator(Enum):
    ADD = '+'
    MUL = '*'
    CON = '||'

def print_equation(numbers, operators, result):
    print(f'{numbers[0]} {" ".join([f"{o.value} {n}" for o, n in zip(operators, numbers[1:])])} = {result}')
    
def sum_valid_equations_results(equations):
    output = 0
    for value, numbers in tqdm(equations):
        for operators in product(list(Operator), repeat=len(numbers)-1): 
            estimation = numbers[0]
            for n, operator in zip(numbers[1:], operators):
                if operator == Operator.ADD:
                    estimation += n
                elif operator == Operator.MUL:
                    estimation *= n
                elif operator == Operator.CON:
                    estimation = int(f'{estimation}{n}')
            if estimation == value:
                output += value
                break

    return output

def main():
    file = sys.argv[1]


    with open(file) as f:
        data = f.read()

        equations = parse_file(data)

        print(sum_valid_equations_results(equations))

if __name__ == '__main__':
    main()