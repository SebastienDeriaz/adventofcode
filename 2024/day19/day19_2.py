import sys
import re
from functools import cache


def parse_data(data):
    desired_patterns = []
    for i, line in enumerate(data.split('\n')):
        if i == 0:
            patterns = line.replace(' ', '').split(',')

        elif i > 1:
            desired_patterns.append(line)

    return patterns, desired_patterns





def main():
    file = sys.argv[1]
    with open(file) as f:
        data = f.read()
        patterns, desired_patterns = parse_data(data)

        @cache
        def possibilities(desired_pattern : str):
            count = 0
            for p in patterns:
                pattern_match = desired_pattern.startswith(p)
                #print(f'{p} in {desired_pattern} : {pattern_match}')
                if len(desired_pattern) == len(p) and pattern_match:
                    count += 1
                elif len(desired_pattern) > len(p) and pattern_match:
                    # test other combinations
                    count += possibilities(desired_pattern[len(p):])

            return count

        possible = 0
        for dp in desired_patterns:
            p = possibilities(dp)
            #print(f'{dp} : {p}')
            possible += p

        print(possible)


if __name__ == '__main__':
    main()