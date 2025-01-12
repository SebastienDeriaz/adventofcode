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

@cache
def sequences(input_sequence, N : int, *, numeric : bool = True):
    keypad = NUMERIC_KEYPAD if numeric else DIRECTIONAL_KEYPAD
    p = np.array(keypad[PRESS])
    output = [input_sequence, '']

    for i, s in enumerate(input_sequence):
        # Create a new sequence
        next_p = np.array(keypad[s])
        v = next_p - p
        x, y = v
        
        left_right = (LEFT*(-x) if x < 0 else RIGHT*x)
        up_down = (DOWN*(-y) if y < 0 else UP*y)

        left_right_first = left_right + up_down + PRESS
        if N > 0: # Evaluate next sequences
            s1 = sequences(left_right_first, N-1, numeric=False)
            up_down_first = up_down + left_right + PRESS
            s2 = sequences(up_down_first, N-1, numeric=False)

            s2len = len(s2[-1])
            s1len = len(s1[-1])
            invalids1 = not valid(s1[0], keypad, p)
            invalids2 = not valid(s2[0], keypad, p)
            if (s2len < s1len and not invalids2) or invalids1:
                s1 = s2
            
            for i in range(len(s1)):
                while len(output) == i+1:
                    output.append('')
                output[i+1] += s1[i]
        else:
            output[1] += left_right_first
    
        p = next_p

    return output

def parse_data(data):
    codes = []
    for line in data.split('\n'):
        if line:
            codes.append(line)
        
    return codes

def main():
    file = sys.argv[1]
    with open(file) as f:
        codes = parse_data(f.read())

    N = 2
    total_complexity = 0
    for code in codes:
        s = sequences(code, N)
        numeric_code = int(''.join([x for x in code if x.isdigit()]))
        print(f'{code} : {len(s[-1])}')
        complexity = numeric_code * len(s[-1])
        total_complexity += complexity

    print(total_complexity)
    


if __name__ == '__main__':
    main()