


from sys import argv
import re

def main():
    file = argv[1]

    with open(file) as f:
        data = f.read()

    total = 0
    enabled = True
    for expression in re.findall("(don't\(\)|mul\((\d{1,3}),(\d{1,3})\)|do\(\))", data):
        if expression[0].startswith("don't"):
            enabled = False
        elif expression[0].startswith("do"):
            enabled = True
        elif expression[0].startswith("mul") and enabled:
            total += int(expression[1]) * int(expression[2])
            

    print(total)


if __name__ == '__main__':
    main()