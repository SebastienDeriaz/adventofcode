import sys

def parse_data(data):
    return [int(x) for x in data.split('\n')]


def mix(secret_number, new_number):
    return secret_number ^ new_number

def prune(new_number):
    return new_number % 16777216


def sequence(secret_number, N):
    number = secret_number
    for i in range(N):
        number = prune(mix(number, number * 64))
        number = prune(mix(number, number // 32))
        number = prune(mix(number, number * 2048))
        yield number

def main():
    file = sys.argv[1]
    with open(file) as f:
        data = f.read()
        codes = parse_data(data)

        total = 0
        for code in codes:
            total += list(sequence(code, 2000))[-1]

        print(total)

if __name__ == '__main__':
    main()