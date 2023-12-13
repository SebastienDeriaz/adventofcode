from sys import argv
import numpy as np

SYMBOLS = {
    '.' : 0,
    '#' : 1
}

def parse_patterns(data):
    patterns = []
    for pattern in data.split('\n\n'):
        patterns.append(np.array([[SYMBOLS[c] for c in line] for line in pattern.split('\n') if line != '']))
    return patterns

def hash(matrix, axis):
    coefficients = 2**np.arange(matrix.shape[axis])
    coef_matrix = coefficients.reshape(-1, 1) @ np.ones([1, matrix.shape[1-axis]])
    if axis > 0:
        coef_matrix = coef_matrix.T
    
    return np.sum(matrix * coef_matrix, axis=axis)

def array_almost_equal(A, B):
    # Check if the difference between A and B is smaller or equal to one single bit on one single comparison max
    diffs = np.abs(A - B).astype(np.uint32)
    if np.count_nonzero(diffs) == 1:
        # Only one difference
        # The difference has to be only 1 bit different
        n = int(np.sum(diffs))
        if n & (n-1) == 0 and n != 0:
            return True
    return False
    

def hash_symetry(h):
    for i in range(1, h.size):
        width = min(i, h.size-i)
        A = h[i-width:i]
        B = h[i:i+width]
        if array_almost_equal(A, B[::-1]):
            return i
    return -1




def main():
    file = argv[1]
    with open(file) as f:
        data = f.read()
        patterns = parse_patterns(data)

        N = 0
        for pattern in patterns:
            for axis in [0, 1]:
                h = hash(pattern, axis)
                s = hash_symetry(h)
                if s > -1:
                    multiplier = (1 if axis == 0 else 100)
                    N += s * multiplier
                    break            
        print(N)

            



if __name__ == '__main__':
    main()