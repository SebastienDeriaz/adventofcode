from sys import argv
import numpy as np


WORD = 'MAS'

R_DIRECTIONS = [1, -1]

def valid_index(array : np.ndarray, r : int, c : int):
    return 0 <= r < array.shape[0] and 0 <= c < array.shape[1]

def find_centered_word_pair_in_directions(array, r, c, direction1, direction2, word):

    dr1, dc1 = direction1
    dr2, dc2 = direction2
    assert len(word) % 2 == 1, "Length cannot be even"
    start = -(len(word) - 1) // 2
    end = (len(word) - 1) // 2
    for w, k in zip(word, range(start, end + 1)):
        ri1 = r+dr1*k
        ci1 = c+dc1*k
        ri2 = r+dr2*k
        ci2 = c+dc2*k
        if not (valid_index(array, ri1, ci1) and array[ri1, ci1] == w):
            break
        if not (valid_index(array, ri2, ci2) and array[ri2, ci2] == w):
            break
    else:
        return True
    return False

def count_word(array : np.ndarray, word : str):
    word_count = 0
    for r in range(array.shape[0]):
        for c in range(array.shape[1]):
            for dr1 in R_DIRECTIONS:
                dc1 = dr1 # First word vector
                for dr2 in [dr1, -dr1]:
                    dc2 = -dr2
                    if find_centered_word_pair_in_directions(array, r, c, (dr1, dc1), (dr2, dc2), WORD):
                        word_count += 1
                        #print(f'Found at [{r},{c}] ({dr1:+n},{dc1:+n})/({dr2:+n},{dc2:+n})')

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