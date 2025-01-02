import sys
import re
import numpy as np
from enum import Enum
from itertools import chain, permutations

UP = '^'
DOWN = 'v'
RIGHT = '>'
LEFT = '<'
PRESS = 'A'
GAP = ' '

DIRECTIONAL_KEYPAD = {
    UP : (0, 1),
    DOWN : (1, 1),
    RIGHT : (1, 2),
    LEFT : (1, 0),
    PRESS : (0, 2),
    GAP : (0, 0)
}

def find_on_keypad(keypad : dict, position):
    for k, p in keypad.items():
        if np.array_equal(p, position):
            return k
    return None

DIRECTIONAL_KEYPAD_EFFECTS = {
    UP : (-1, 0),
    DOWN : (1, 0),
    RIGHT : (0, 1),
    LEFT : (0, -1)
}

NUMERIC_KEYPAD = {
    GAP : (3, 0),
    PRESS : (3, 2),
    0 : (3, 1), 
    1 : (2, 0),
    2 : (2, 1),
    3 : (2, 2),
    4 : (1, 0),
    5 : (1, 1),
    6 : (1, 2),
    7 : (0, 0),
    8 : (0, 1),
    9 : (0, 2),
}

def move_cost(keypad : dict, moves : list):
    # Start at A
    p = np.array(DIRECTIONAL_KEYPAD[PRESS])
    cost = 0
    for m in moves + [PRESS]:
        p2 = np.array(DIRECTIONAL_KEYPAD[m])
        d = p2 - p
        p = p2
        c = np.sum(np.abs(d))
        cost += c

    return cost

def best_move(keypad : dict, moves : list):
    moves_list = []
    for permutation in permutations(moves, len(moves)):
        cost = move_cost(keypad, list(permutation))
        moves_list.append((permutation, cost))

        # p = np.array(keypad[start])
        # for m in permutation:
        #     p += np.array(DIRECTIONAL_KEYPAD[m])
        #     if np.array_equal(p, keypad[GAP]):
        #         print(f'Move {permutation} starting at {start} is illegal')
        #         cost = 1000000


    moves_list.sort(key=lambda x : x[1])
    output = list(moves_list[0][0])
    #print(f'Best move : {moves_list[0]}')
    return output


def directional_moves_per_vector(keypad : dict, v : np.ndarray):
    moves = []
    # for _ in range(np.abs(v[1])):
    #     moves.append(RIGHT if v[1] > 0 else LEFT)
    # for _ in range(np.abs(v[0])):
    #     moves.append(DOWN if v[0] > 0 else UP)
    
    condition = ((keypad == NUMERIC_KEYPAD) ^ (v[0] < 0))
    condition = v[0] < 0
    condition = ((keypad == NUMERIC_KEYPAD) ^ (v[0] < 0))
    if condition:
        for _ in range(np.abs(v[1])):
            moves.append(RIGHT if v[1] > 0 else LEFT)
        for _ in range(np.abs(v[0])):
            moves.append(DOWN if v[0] > 0 else UP)
    else:
        for _ in range(np.abs(v[0])):
            moves.append(DOWN if v[0] > 0 else UP)
        for _ in range(np.abs(v[1])):
            moves.append(RIGHT if v[1] > 0 else LEFT)

    return moves

def keypad_moves(code : list, keypad : dict):
    movements = []
    # Start
    p = np.array(keypad[PRESS])
    for c in code:
        movements.append([])
        # Calculate the vector
        if c == ' ':
            continue
        v = np.array(keypad[c]) - p

        moves = directional_moves_per_vector(keypad, v)
        
#        print(f'To obtain {c}, the moves are {moves}')

        movements[-1] += best_move(keypad, moves)
        #movements[-1] += moves
        movements[-1].append(PRESS)
        p = np.array(keypad[c])
 #       input()

    return movements

def parse_data(data):
    codes = []
    for line in data.split('\n'):
        codes.append([int(x) if x.isdecimal() else x for x in line])
    return codes


def simulate(sequence, layers):
    sequence = sequence.copy()
    sequences = [sequence.copy()]
    for layer in range(0, layers)[::-1]:
        keys = []
        keypad = NUMERIC_KEYPAD if layer == 0 else DIRECTIONAL_KEYPAD
        p = np.array(keypad[PRESS])

        for s in sequence:
            if np.array_equal(p, keypad[GAP]):
                raise ValueError('Crashed')
            if s == PRESS:
                key = find_on_keypad(keypad, p)
                keys.append(key)
            else:
                p += DIRECTIONAL_KEYPAD_EFFECTS[s]
        sequence = keys
        sequences.append(keys.copy())

    return keys, sequences

def spaced_list(code):
    return ' '.join([''.join(lst) for lst in code])

def to_list(code):
    output = []
    for lst in code:
        output += lst
    return output


VALID_CODES = {
    '029A': '<vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A',
    '980A': '<v<A>>^AAAvA^A<vA<AA>>^AvAA<^A>A<v<A>A>^AAAvA<^A>A<vA>^A<A>A',
    '179A': '<v<A>>^A<vA<A>>^AAvAA<^A>A<v<A>>^AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A',
    '456A': '<v<A>>^AA<vA<A>>^AAvAA<^A>A<vA>^A<A>A<vA>^A<A>A<v<A>A>^AAvA<^A>A',
    '379A': '<v<A>>^AvA^A<vA<AA>>^AAvA<^A>AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A',
}

def disp_sim(x, master):
    output = ''
    x_iter = iter(x)
    try:
        for m in master:
            if m != ' ':
                output += next(x_iter)
            else:
                output += ' '
    except StopIteration:
        pass
    
    return output




def main():
    file = sys.argv[1]
    with open(file) as f:
        codes = parse_data(f.read())

    total_complexity = 0
    for code in codes:
        robot_1 = keypad_moves(code, keypad=NUMERIC_KEYPAD)
        robot_2 = keypad_moves(chain(*robot_1), keypad=DIRECTIONAL_KEYPAD)
        human = keypad_moves(chain(*robot_2), keypad=DIRECTIONAL_KEYPAD)
        #human = keypad_moves(robot_3, keypad=DIRECTIONAL_KEYPAD)
        numeric_code = int(''.join([str(x) for x in code if isinstance(x, int)]))


        code_str = "".join([str(x) for x in code])

        valid_sequence = VALID_CODES["".join(code_str)]
        result_sim, simulations = simulate(list(valid_sequence), 3)

        result_confirmation, _ = simulate(to_list(human), 3)


        assert result_confirmation == code

        print(f'  Code          : {code_str}')
        print(f'  Code (sim)    : {"".join([str(x) for x in result_sim])}')
        print(f'  Robot 1       : {spaced_list(robot_1)}')
        print(f'  Robot 1 (sim) : {disp_sim(simulations[2], spaced_list(robot_1))}')
        print(f'  Robot 2       : {spaced_list(robot_2)}')
        print(f'  Robot 2 (sim) : {disp_sim(simulations[1], spaced_list(robot_2))}')
        print(f'  Human         : {spaced_list(human)}')
        print(f'  Human (sim)   : {disp_sim(simulations[0], spaced_list(human))}')
        len_human = sum(len(lst) for lst in human)
        complexity = numeric_code * len_human
        #print(f"{''.join([str(x) for x in code])} : {spaced_list(human)}")
        print(f'  Complexity : {len_human} * {numeric_code}  = {complexity}')
        total_complexity += complexity

    print(total_complexity)
    


if __name__ == '__main__':
    main()