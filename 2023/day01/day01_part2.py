from sys import argv, stdin

SPELLED_NUMBERS = {
    'zero' : '0',
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
    words_indices = {k : 0 for k in SPELLED_NUMBERS}
    for c in line:
        if is_digit(c):
            fragments.append(c)
            words_indices = {k : 0 for k in words_indices}
        else:
            for word, idx in words_indices.items():
                if c == word[idx]:
                    # This one is correct, increment its index
                    words_indices[word] += 1
                    if words_indices[word] == len(word):
                        # If we've completed the word
                        fragments.append(SPELLED_NUMBERS[word])
                        # Reset the word
                        words_indices[word] = 0
                elif idx == 1 and c == word[idx-1]:
                    # Don't do anything
                    pass
                else:
                    # Reset otherwise
                    words_indices[word] = 0
    return fragments

def decode_calibration_values(document : str) -> list:
    # Split by lines
    LINE_END = '\n'
    
    values = []

    for line in document.split(LINE_END):
        fragments = decode_line(line)
        if fragments:
            number = int(fragments[0] + fragments[-1])
            values.append(number)
    return values


def main():
    if len(argv) > 1:
        argument = argv[1]
        if '.' in argument:
            with open(argument) as f:
                data = f.read()
        else:
            data = argument
    else:
        # Read stdin
        data = stdin.read()
    
    result = sum(decode_calibration_values(data))
    print(result)


if __name__ == '__main__':
    main()