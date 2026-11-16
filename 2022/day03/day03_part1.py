import sys
import numpy as np

def priority(letter : str) -> int:
    o = ord(letter)
    if ord('a') <= o <= ord('z'):
        return o - ord('a') + 1
    elif ord('A') <= o <= ord('Z'):
        return o - ord('A') + 27
    else:
        raise ValueError(f"No priority for '{letter}'")

def main():
    file = sys.argv[1]
    with open(file) as f:
        data = f.read()

    backpacks = data.split('\n')

    total = 0
    for backpack in backpacks:
        numeric_backpack = [ord(x) for x in backpack]

        left = np.unique(np.array(numeric_backpack[:len(numeric_backpack)//2]))
        right = np.unique(np.array(numeric_backpack[len(numeric_backpack)//2:]))

        unique_values = np.concatenate([left, right])
        unique_values.sort()

        in_both_sides = unique_values[:-1][np.diff(unique_values) == 0]

        total += sum([priority(chr(x)) for x in in_both_sides])

    print(total)

if __name__ == '__main__':
    main()
