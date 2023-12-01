def decode_calibration_values(document : str) -> list:
    # Split by lines
    LINE_END = '\n'
    def is_digit(x):
        return '0' <= x <= '9'
    values = []

    for line in document.split(LINE_END):
        print(f"Line {line}")
        digits = list(filter(is_digit, line))
        print(f"Digits {digits}")
        number = int(digits[0] + digits[-1])
        print(f"Calibration value : {number}")
        values.append(number)
    return values


def main():
    with open('input.txt') as f:
        result = sum(decode_calibration_values(f.read()))
        print(f"Sum of all calibration values : {result}")


if __name__ == '__main__':
    main()