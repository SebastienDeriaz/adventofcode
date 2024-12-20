import re
import sys
from enum import Enum
import matplotlib.pyplot as plt
import numpy as np


DICHOMOTOMY = True

class Instruction(Enum):
    ADV = 0
    BXL = 1
    BST = 2
    JNZ = 3
    BXC = 4
    OUT = 5
    BDV = 6
    CDV = 7

class OperandValue(Enum):
    REGISTER_A = 4
    REGISTER_B = 5
    REGISTER_C = 6
    

class State(Enum):
    SEARCH_LEFT = 0
    FOUND_LEFT = 1
    #FOUND_RIGHT = 2


def parse_data(data):
    registers = {}
    for x in 'ABC':
        register_pattern = f'Register {x}: (\d+)'
        value = int(re.findall(register_pattern, data)[0])
        registers[x] = value

    PROGRAM_PATTERN = 'Program: ([\d,]+)'
    
    program = re.findall(PROGRAM_PATTERN, data)[0]

    program = [int(x) for x in program.split(',')]
    return registers, program


def run(registers, program):
    ip = 0
    outputs = []
    while True:
        if ip >= len(program):
            break
        opcode = Instruction(program[ip])
        ip += 1
        if ip >= len(program):
            break
        operand = program[ip]
        ip += 1

        if operand ==  OperandValue.REGISTER_A.value:
            combo_operand = registers['A']
        elif operand == OperandValue.REGISTER_B.value:
            combo_operand = registers['B']
        elif operand == OperandValue.REGISTER_C.value:
            combo_operand = registers['C']
        else:
            combo_operand = operand

        if opcode == Instruction.ADV: # 0
            #old_value = registers['A']
            registers['A'] = registers['A'] // (2**combo_operand)
            #print('ADV')
            #print(f' A {old_value} -> {old_value} / 2**({combo_operand})={registers["A"]}')
        elif opcode == Instruction.BXL: # 1
            #print('BXL')
            #old_value = registers['B']
            registers['B'] = registers['B'] ^ operand
            #print(f' B {old_value} -> B^{operand}={registers["B"]}')
        elif opcode == Instruction.BST: # 2
            #print('BST')
            #old_value = registers['B']
            registers['B'] = combo_operand % 8
            #print(f' B {old_value} -> {combo_operand} % 8 = {registers["B"]}')
        elif opcode == Instruction.JNZ: # 3
            #print('JNZ')
            if registers['A'] != 0:
                #print('  JUMP')
                ip = operand
            else:
                #print('  Do nothing')
                ...
        elif opcode == Instruction.BXC: # 4
            #print('BXC')
            #old_value = registers["B"]
            registers['B'] = registers['B'] ^ registers['C']
            #print(f' B {old_value} -> {old_value}^{registers["C"]}={registers["B"]}')
            # Ignore the operand
        elif opcode == Instruction.OUT: # 5
            #print('OUT')
            value = combo_operand % 8
            #print(f' {combo_operand} % 8 = {value}')
            outputs.append(value)
        elif opcode == Instruction.BDV:
            registers['B'] = registers['A'] // (2**combo_operand)            
        elif opcode == Instruction.CDV:
            registers['C'] = registers['A'] // (2**combo_operand)

    return outputs


def main():
    file = sys.argv[1]
    with open(file) as f:
        registers, program = parse_data(f.read())        

        if DICHOMOTOMY:

            start = 35184372088832
            end = 281474976710655

            def test(a, i):
                registers.update({'A' : a})
                output = run(registers, program)
                return output[i:] == program[i:]
            e = end
            s = start

            regions = [[s, e]]

            i = len(program) - 1
            # Find the last number, then the previous, etc...
            N = 1000
            while True:

                new_regions = []
                for region in regions:
                    s, e = region
                    state = State.SEARCH_LEFT
                    # Subdivide the region in N segments
                    left = s
                    n_samples = N if (e-s+1 > N) and i != 0 else e-s+1

                    #print(f'Samples : {n_samples}')
                    for k in np.linspace(s, e, n_samples):
                        k = int(k)
                        test_result = test(k, i)
                        #print(f'{k=} {"ok" if test_result else "not ok"}')
                        if test_result:
                            if state == State.SEARCH_LEFT:
                                # Create a new region
                                new_regions.append([left])
                                state = State.FOUND_LEFT
                        else:
                            if state == State.SEARCH_LEFT:
                                left = k
                            if state == State.FOUND_LEFT:
                                new_regions[-1].append(k)
                                state = State.SEARCH_LEFT
                                left = k
                    if state == State.FOUND_LEFT:
                        new_regions[-1].append(e)
                    
                if len(new_regions) == 0:
                    # Couldn't find a match, subdivide
                    raise ValueError('No ok zone was found')

                regions = new_regions.copy()
                if i == 0:
                    break
                else:
                    s = new_regions[0][0]
                    e = new_regions[-1][1]
                    i -= 1


            regions.sort(key=lambda x : x[0])
            a = regions[0][0]+1
            print(a)


if __name__ == '__main__':
    main()
