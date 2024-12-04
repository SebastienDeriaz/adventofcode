from sys import argv
import numpy as np


WORD = 'XMAS'

XY_DIRECTIONS = [-1, 0, 1]

def valid_index(array : np.ndarray, r : int, c : int):
    return 0 <= r < array.shape[0] and 0 <= c < array.shape[1]

def get_word_in_direction(array, r, c, direction, length):
    word = ''
    dr, dc = direction
    for k in range(length):
        ri = r+dr*k
        ci = c+dc*k
        if valid_index(array, ri, ci):
            word += array[ri, ci]
    return word

def count_word(array : np.ndarray, word : str):
    word_count = 0
    for r in range(array.shape[0]):
        for c in range(array.shape[1]):
            for dr in XY_DIRECTIONS:
                for dc in XY_DIRECTIONS:
                    if get_word_in_direction(array, r, c, (dr, dc), len(WORD)) == WORD:
                        word_count += 1

    return word_count


            

def main():
    file = argv[1]

    with open(file) as f:
        data = f.read()

        lines = [list(x) for x in list(filter(None, data.split('\n')))]
        array = np.array(lines)
        

        print(count_word(array, WORD))
        


if __name__ == '__main__':
    main()