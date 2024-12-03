from sys import argv
import re

def main():
    file = argv[1]

    with open(file) as f:
        data = f.read()

    total = 0
    for x, y in re.findall('mul\((\d{1,3}),(\d{1,3})\)', data):
        total += int(x) * int(y)

    print(total)


if __name__ == '__main__':
    main()