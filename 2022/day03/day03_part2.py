import numpy as np
from collections import Counter
import sys
from day03_part1 import priority

def main():
    file = sys.argv[1]
    with open(file) as f:
        data = f.read()

    backpacks = data.split('\n')

    groups = [backpacks[3*i:3*(i+1)] for i in range(len(backpacks)//3)]

    total = 0
    for group in groups:
        counts = Counter(
            np.concatenate(
                [np.unique([ord(x) for x in backpack]) for backpack in group]
            )
        )

        badge = chr(counts.most_common()[0][0])

        total += priority(badge)

    print(total)
        





    


if __name__ == '__main__':
    main()