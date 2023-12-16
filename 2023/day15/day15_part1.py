from sys import argv
from functools import reduce

def parse_sequence(data):
    return [step for step in data.replace('\n', '').split(',') if step != '']

def hash_step(step):
    def f(n, b):
        return ((n + ord(b)) * 17) % 256
    return reduce(f, step, 0)

def main():
    file = argv[1]
    with open(file) as f:
        data = f.read()
        steps = parse_sequence(data)
        print(sum([hash_step(s) for s in steps]))

if __name__ == '__main__':
    main()