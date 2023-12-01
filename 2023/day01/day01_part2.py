SPELLED_NUMBERS = {
    'one' : '1',
    'two' : '2',
    'three' : '3',
    'four' : '4',
    'five' : '5',
    'six' : '6',
    'seven' : '7',
    'eight' : '8',
    'nine' : '9'
}

def is_digit(x):
    return '0' <= x <= '9'

def decode_line(line) -> list:
    fragments = []
    words_indices = {k : 0 for k in SPELLED_NUMBERS.values()}

    for c in line:
        if is_digit(c):
            fragments.append(c)
            words_indices = {k : 0 for k in words_indices}
        else:
            for word, idx in words_indices.items():
                if c == word[idx]:
                    print(f"{c} in {word}")
                    # This one is correct, increment its index
                    words_indices[word] += 1
                    if words_indices[word] == len(word):
                        # If we've completed the word
                        fragments.append(SPELLED_NUMBERS[word])
                        # Reset the words_indices
                        words_indices = {k : 0 for k in words_indices}
    return fragments

def decode_calibration_values(document : str) -> list:
    # Split by lines
    LINE_END = '\n'
    
    values = []

    for line in document.split(LINE_END):
        print(f"Line {line}")
        fragments = decode_line(line)
        number = int(fragments[0] + fragments[-1])
        print(f"Calibration value : {number}")
        values.append(number)
    return values


def main():
    with open('input.txt') as f:
        result = sum(decode_calibration_values(f.read()))
        print(f"Sum of all calibration values : {result}")


if __name__ == '__main__':
    main()