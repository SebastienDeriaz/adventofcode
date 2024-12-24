import sys
import re
from enum import Enum
from dataclasses import dataclass

class GateType(Enum):
    XOR = 'XOR'
    OR = 'OR'
    AND = 'AND'

@dataclass
class Gate:
    in1 : str
    in2 : str
    operation : GateType

    def __post_init__(self): 
        self.operation = GateType(self.operation)
        

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
    if v in initial:
        return initial[v]
    elif v in gates:
        # Calculate value
        gate : Gate
        gate = gates[v]
        a = solve(gate.in1, gates, initial)
        b = solve(gate.in2, gates, initial)
        if gate.operation == GateType.AND:
            return a and b
        elif gate.operation == GateType.OR:
            return a or b
        elif gate.operation == GateType.XOR:
            return a ^ b
    else:
        raise ValueError(f'Value {v} is not controlled')


def main():
    initial, gates = parse_file(sys.argv[1])
    
    output_values = {x : solve(x, gates, initial) for x in sorted(filter(lambda x : x.startswith('z'), gates))}

    value = sum([2**i * x for i, x in enumerate(output_values.values())])

    print(value)

if __name__ == '__main__':
    main()