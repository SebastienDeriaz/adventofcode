import sys
import re


def parse_data(data):
    desired_patterns = []
    for i, line in enumerate(data.split('\n')):
        if i == 0:
            patterns = line.replace(' ', '').split(',')

        elif i > 1:
            desired_patterns.append(line)

    return patterns, desired_patterns


def valid(patterns : list, desired_pattern : str):
    for p in patterns:
        pattern_match = desired_pattern.startswith(p)
        if len(desired_pattern) == len(p) and pattern_match:
            return True
        elif len(desired_pattern) > len(p) and pattern_match:
            # test other combinations
            if(valid(patterns, desired_pattern[len(p):])):
                return True

    return False


def main():
    file = sys.argv[1]
    with open(file) as f:
        data = f.read()
        patterns, desired_patterns = parse_data(data)

        possible = sum([valid(patterns, dp) for dp in desired_patterns])        

        print(possible)


if __name__ == '__main__':
    main()