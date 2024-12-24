import sys
import re
from enum import Enum
from dataclasses import dataclass
import math

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
        solved_gates[v] = initial[v]
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

        self.output_gates = [f'z{i:02}' for i in range(N+1)]


    def set_swaps(self, swaps : list):
        self.swapped_gates = self.gates.copy()
        for a, b in swaps:
            self.swapped_gates[a], self.swapped_gates[b] = self.swapped_gates[b], self.swapped_gates[a]

    def calc(self, x, y) -> int:
        initial = {}
        for n in range(self.N):
            initial[f'x{n:02}'] = (x >> n) & 0x01
            initial[f'y{n:02}'] = (y >> n) & 0x01

        output_values = {x : solve(x, self.swapped_gates, initial) for x in self.output_gates}
        
        gates = {}

        for output_gate, (z, gate_values) in output_values.items():
            gates[output_gate] = {}
            for gate, value in gate_values.items():
                gates[output_gate][gate] = value

        return sum([2**i * x for i, (x, _) in enumerate(output_values.values())]), gates


def ab_generator(N):
    for i in range(N):
        for j in range(N):
            yield 1 << i, 1 << j

def main():
    _, gates = parse_file(sys.argv[1])

    # Number of inputs
    N = len([x for x in gates if x.startswith('z')]) - 1
    print(f'Number of gates : {len(gates)}')
    print(f'Number of inputs : {N}')

    calculator = Calculator(gates, 45)

    calculator.set_swaps([('z05', 'jst'), ('mcm', 'gdf'), ('z15', 'dnt'), ('gwc', 'z30')])

    nc = math.ceil(math.log10(2**(N+1)-1))

    for a, b in ab_generator(N):
        output, _ = calculator.calc(a, b)

        expected_output = a + b
        valid = output == expected_output
        print(f'a={a:{nc}d} b={b:{nc}d} : {output:{nc}}/{expected_output} {"✅" if valid else "❌"}')

if __name__ == '__main__':
    main()