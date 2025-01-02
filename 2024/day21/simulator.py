import numpy as np


UP = '^'
DOWN = 'v'
RIGHT = '>'
LEFT = '<'
PRESS = 'A'

DIRECTIONAL_KEYPAD = {
    UP : (1, 1),
    PRESS : (2, 1),
    RIGHT : (2, 0),
    DOWN : (1, 0),
    LEFT : (0, 0),
}

def find_on_keypad(keypad : dict, position):
    for k, p in keypad.items():
        if np.array_equal(p, position):
            return k
    return None

DIRECTIONAL_KEYPAD_EFFECTS = {
    UP : (0, 1),
    DOWN : (0, -1),
    RIGHT : (1, 0),
    LEFT : (-1, 0)
}

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
}


def simulate(sequence, numeric : bool = False):
    keypad = NUMERIC_KEYPAD if numeric else DIRECTIONAL_KEYPAD
    
    output_sequence = ''
    p = np.array(keypad[PRESS])

    for s in sequence:
        if find_on_keypad(keypad, p) is None:
            raise ValueError('Crashed')
        if s == PRESS:
            key = find_on_keypad(keypad, p)
            output_sequence += key
        else:
            p += DIRECTIONAL_KEYPAD_EFFECTS[s]

    return output_sequence