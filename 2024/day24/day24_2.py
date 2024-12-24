import sys
import re
from enum import Enum
from dataclasses import dataclass
from random import randint
from time import sleep

class Operation(Enum):
    XOR = 'XOR'
    OR = 'OR'
    AND = 'AND'
    

class GateStatus(Enum):
    VALID = 0
    UNKNOWN = 1
    INVALID = 2

@dataclass
class Gate:
    in1 : str
    in2 : str
    operation : Operation

    def __post_init__(self): 
        self.operation = Operation(self.operation)
        

def parse_file(file):
    INITIAL_PATTERN = '(\w+): ([01])'
    GATE_PATTERN = '(\w+) (\w+) (\w+) -> (\w+)'
    initial = {}
    gates = {}
    with open(file) as f:
        data = f.read()
        # Find initial conditions
        for name, value in re.findall(INITIAL_PATTERN, data):
            initial[name] = int(value)
        # Find gates
        for a, op, b, result in re.findall(GATE_PATTERN, data):
            gates[result] = Gate(a, b, op)


    return initial, gates


def solve(v, gates, initial):
    solved_gates = {}
    if v in initial:
        #solved_gates[v] = initial[v]
        return initial[v], solved_gates
    elif v in gates:
        # Calculate value
        gate : Gate
        gate = gates[v]
        a, a_solved_gates = solve(gate.in1, gates, initial)
        b, b_solved_gates = solve(gate.in2, gates, initial)
        solved_gates.update(a_solved_gates)
        solved_gates.update(b_solved_gates)
        if gate.operation == Operation.AND:
            solution = a and b
        elif gate.operation == Operation.OR:
            solution = a or b
        elif gate.operation == Operation.XOR:
            solution = a ^ b
        solved_gates[v] = solution
        return solution, solved_gates
    else:
        raise ValueError(f'Value {v} is not controlled')

class Calculator:
    def __init__(self, gates : dict, N : int) -> None:
        self.gates = gates
        self.swapped_gates = self.gates.copy()
        self.N = N


    def swap(self, swaps : list):
        self.swapped_gates = self.gates.copy()
        for a, b in swaps:
            self.swapped_gates[a], self.swapped_gates[b] = self.swapped_gates[b], self.swapped_gates[a]

    def calc(self, x, y) -> int:
        initial = {}
        for n in range(self.N):
            initial[f'x{n:02}'] = (x >> n) & 0x01
            initial[f'y{n:02}'] = (y >> n) & 0x01


        output_values = {x : solve(x, self.swapped_gates, initial) for x in sorted(filter(lambda x : x.startswith('z'), self.swapped_gates))}
        
        gates = {}

        for z, gate_values in output_values.values():
            for gate, value in gate_values.items():
                gates[gate] = value

        return sum([2**i * x for i, (x, _) in enumerate(output_values.values())]), gates





def wrong_inputs_per_wrong_gate(gate : Gate, false_value):
    if gate.operation == Operation.AND:
        if false_value == 0:
            # Both gate are false
            return [gate.in1, gate.in2]
        # Cannot tell otherwise
    elif gate.operation == Operation.OR:
        if false_value == 1:
            # Both gate are false
            return [gate.in1, gate.in2]
        # Cannot tell otherwise
    elif gate.operation == Operation.XOR:
        pass


def backtrack_score(gate : Gate, valid_value):
    score = 1
    if gate.operation == Operation.AND and valid_value == 1:
        score = 2
    elif gate.operation == Operation.OR and valid_value == 0:
        score = 2
    return score


def generate_expected_gates(gates : dict, initials : dict, expected_gates : dict, gate_name : str, valid_output : int):
    expected_gates[gate_name] = valid_output
    gate = gates[gate_name]

    if gate.in1 in initials:
        expected_gates[gate.in1] = initials[gate.in1]
    if gate.in2 in initials:
        expected_gates[gate.in2] = initials[gate.in2]
    
    # If both input gates are unknown
    in1_known = gate.in1 in expected_gates
    in2_known = gate.in2 in expected_gates
    
    if not in1_known and not in2_known:
        # If nothing is known, only do the obvious
        if gate.operation == Operation.AND and valid_output == 1:
            # Inputs are 1
            generate_expected_gates(gates, initials, expected_gates, gate.in1, 1)
            generate_expected_gates(gates, initials, expected_gates, gate.in2, 1)
        elif gate.operation == Operation.OR and valid_output == 0:
            generate_expected_gates(gates, initials, expected_gates, gate.in1, 0)
            generate_expected_gates(gates, initials, expected_gates, gate.in2, 0)
    elif in1_known and not in2_known:
        in1 = expected_gates[gate.in1]
        if gate.operation == Operation.OR and in1 == 0:
            generate_expected_gates(gates, initials, expected_gates, gate.in2, 0)
        elif gate.operation == Operation.AND and in1 == 1:
            generate_expected_gates(gates, initials, expected_gates, gate.in2, 1)
        elif gate.operation == Operation.XOR:
            generate_expected_gates(gates, initials, expected_gates, gate.in2, valid_output ^ in1)
    else:
        # Both are known, nothing to do
        pass
        
        


def main():
    initials, gates = parse_file(sys.argv[1])
    
    # Number of inputs
    N = len([x for x in gates if x.startswith('z')]) - 1
    print(f'Number of gates : {len(gates)}')
    print(f'Number of inputs : {N}')

    calculator = Calculator(gates, 45)

    possible_gate_swaps = {gate : [x for x in list(gates.keys()) if x != gate] for gate in gates}

    def score():
        return sum([len(swaps) for swaps in possible_gate_swaps.values()])
    
    #for i in range(N):
    s = 0
    print(score())
    tries = 100000
    while tries:
        a = randint(0, 2**(N+1)-1)
        b = randint(0, 2**(N+1)-1)
        #print(f'{a=}, {b=}')
        #a = 1 << i
        #b = 0
        expected_output = a + b
        output, calculated_gates = calculator.calc(a, b)


        expected_gates = {}
        # Generate a gate tree of known values based on the expected value
        for i in range(N+1):
            while True:
                L = len(expected_gates)
                generate_expected_gates(gates, initials, expected_gates, f'z{i:02}', (expected_output >> i) & 0x01)
                if len(expected_gates) == L:
                    break

        #print(f'Known gates : {len(expected_gates)} / {len(gates)} ({len(expected_gates) / len(gates):.2%})')

        for g in gates:
            if gates[g].operation == Operation.AND:
                print('&', end='')
            elif gates[g].operation == Operation.XOR:
                print('^', end='')
            elif gates[g].operation == Operation.OR:
                print('+', end='')
        print()
        for g in gates:
            if g in expected_gates:
                print('#', end='')
            else:
                print('.', end='')

        print()
        for g in gates:
            if g.startswith('z'):
                number = int(g.strip('z'))
                print((expected_output >> number) & 0x01, end='')
            else:
                print(' ', end='')
        
        print()
 
        #print(f'To get {expected_output}, these are the known gate values : {expected_gates}')


        # Look in the calculated gates and find which one could be swapped

        for A, _ in possible_gate_swaps.items():
            if A in expected_gates:
                if calculated_gates[A] != expected_gates[A]:
                    # If the gate is wrong, remove all of the others that are valid with the same value
                    for gn, value in expected_gates.items():
                        if value == calculated_gates[A]:
                            # This gate CANNOT be the one
                            if gn in possible_gate_swaps[A]:
                                possible_gate_swaps[A].remove(gn)

        s2 = score()
        print(s2)
        if s == s2:
            tries -= 1
        s = s2

        sleep(0.05)


        # for gate, swaps in possible_gate_swaps.items():
        #     print(f'{gate} : {len(swaps)}')


        # print(f'{a:012X} : {output:012X}  {"✅" if valid else "❌"}')

        # gates_to_update = [f'z{i:02}' for i in range(N)]
        # valid_values = {f'z{i:02}' : (output >> i) & 0x01 for i in range(N)}
        # while True:
        #     gate_name = gates_to_update.pop(0)
        #     gate = gates[gate_name]
        #     valid_value = valid_values[gate_name]
        #     z_value = calculated_gates[gate_name][1]

        #     valid = z_value == valid_value
        #     # Update the gate status
        #     calculated_gates[start][0] = GateStatus.VALID if valid else GateStatus.INVALID
        #     # Add the outputs
    


    # Assert calculator works on example 1
    # x_value = sum([2**i * initial[f'x{i:02}'] for i in range(N)])
    # y_value = sum([2**i * initial[f'y{i:02}'] for i in range(N)])
    # day1_value = 47666458872582
    # assert calculator.calc(x_value, y_value) == day1_value, "Calculator has a problem"

if __name__ == '__main__':
    main()