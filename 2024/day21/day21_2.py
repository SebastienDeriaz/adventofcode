import numpy as np
from functools import cache
import sys

PRESS = 'A'
LEFT = '<'
RIGHT = '>'
UP = '^'
DOWN = 'v'
GAP = ' '

NUMERIC_KEYPAD = {
    PRESS : (2, 0),
    '0' : (1, 0),
    '1' : (0, 1),
    '2' : (1, 1),
    '3' : (2, 1),
    '4' : (0, 2),
    '5' : (1, 2),
    '6' : (2, 2),
    '7' : (0, 3),
    '8' : (1, 3),
    '9' : (2, 3),
    GAP : (0, 0)
}

DIRECTIONAL_KEYPAD = {
    LEFT : (0,0),
    DOWN : (1,0),
    RIGHT : (2,0),
    UP : (1,1),
    PRESS : (2, 1),
    GAP : (0, 1)
}

DIRECTIONAL_KEYPAD_ACTIONS = {
    LEFT : (-1, 0),
    RIGHT : (1, 0),
    UP : (0, 1),
    DOWN : (0, -1)
}

def valid(sequence : str, keypad : dict, start : np.ndarray):
    
    p = start.copy()
    for s in sequence:
        if s != PRESS:
            p += DIRECTIONAL_KEYPAD_ACTIONS[s]
            if keypad[GAP] == tuple(p):
                return False
            elif tuple(p) not in keypad.values():
                raise RuntimeError(f'invalid position : {p} ({sequence}, {start}, {keypad})')
    return True

def parse_data(data):
    codes = []
    for line in data.split('\n'):
        if line:
            codes.append(line)
        
    return codes


class SequenceLength:
    def __init__(self) -> None:
        pass
        

    @cache
    def sequence_length(self, input_sequence : str, depth : int, numeric : bool = True):
        #print(f'{" "*(3-depth)} {depth} : {input_sequence}')
        keypad = NUMERIC_KEYPAD if numeric else DIRECTIONAL_KEYPAD
        # If depth == 0, return the sequence itself
        output = 0
        if depth == 0:
            output = len(input_sequence)
        else: 
            p = np.array(keypad[PRESS])

            for s in input_sequence:
                # Create a new sequence
                next_p = np.array(keypad[s])
                v = next_p - p
                x, y = v
                
                left_right = (LEFT*(-x) if x < 0 else RIGHT*x)
                up_down = (DOWN*(-y) if y < 0 else UP*y)

                sequences = [
                    left_right + up_down + PRESS,
                    up_down + left_right + PRESS
                    ]

                sequences = list(filter(lambda s : valid(s, keypad, p), sequences))

                lengths = [self.sequence_length(s, depth-1, numeric=False) for s in sequences]

                if len(lengths) > 0:
                    output += min(lengths)
                else:
                    output = None
                    break
            
                p = next_p


        return output
        

def main():
    file = sys.argv[1]
    with open(file) as f:
        codes = parse_data(f.read())

    sl = SequenceLength()

    N = 26
    total_complexity = 0
    for code in codes:
        numeric_code = int(''.join([x for x in code if x.isdigit()]))
        L = sl.sequence_length(code, N)
        
        #print(f'{code} : {L}')
        complexity = numeric_code * L
        total_complexity += complexity

    print(total_complexity)
    


if __name__ == '__main__':
    main()