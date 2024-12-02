from sys import argv
from itertools import combinations


def is_safe(report : list):
    MIN = 1
    MAX = 3
    diffs = [rb - ra for rb, ra in zip(report[:-1], report[1:])]
    return all([MIN <= x <= MAX for x in diffs]) or all([-MAX <= x <= -MIN for x in diffs])

REMOVABLE_LEVELS = 1


def main():
    file = argv[1]

    with open(file) as f:
        data = f.read()
    

    safe_reports = 0
    for line in data.split('\n'):
        report = [int(x) for x in line.split(' ')]

        for r in range(REMOVABLE_LEVELS+1):
            stop = False
            for comb in combinations(report, len(report) - r):
                if is_safe(comb):
                    safe_reports += 1
                    stop = True
                    break
            if stop:
                break

    print(safe_reports)

if __name__ == '__main__':
    main()