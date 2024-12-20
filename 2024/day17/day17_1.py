import re
import sys
from enum import Enum

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
            old_value = registers['A']
            registers['A'] = registers['A'] // (2**combo_operand)
        elif opcode == Instruction.BXL: # 1
            registers['B'] = registers['B'] ^ operand
        elif opcode == Instruction.BST: # 2
            registers['B'] = combo_operand % 8
        elif opcode == Instruction.JNZ: # 3
            if registers['A'] != 0:
                ip = operand
        elif opcode == Instruction.BXC: # 4
            registers['B'] = registers['B'] ^ registers['C']
            # Ignore the operand
        elif opcode == Instruction.OUT: # 5
            value = combo_operand % 8
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

        print(','.join([str(x) for x in run(registers, program)]))

if __name__ == '__main__':
    main()
