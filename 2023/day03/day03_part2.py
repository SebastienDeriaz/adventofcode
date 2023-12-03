# Some numbers can appear multiple times
# 0 doesn't exist
# 1) Create a number matrix that contains -2 for ".", -1 for symbols and digits for the rest
# 2) For each symbol location, find all the numbers around it (left-most digit)
# 3) Check if it has been added already (cache)
# 4) If not, parse the number (read it from left to right)
# 5) Repeat for each number, each symbol


from sys import argv
import numpy as np
LINE_DELIMITER = '\n'
SYMBOL_NUMBER = -1
SPACER_NUMBER = -2
GEAR_NUMBER = -3

def number_match(x : str):
    if x.isdigit():
        return int(x)
    elif x == '.':
        return SPACER_NUMBER
    elif x == '*':
        return GEAR_NUMBER
    else:
        return SYMBOL_NUMBER

def find_start(M, x, y):
    # Left-find mode
    x_search = x
    while x_search > 0 and M[y, x_search-1] <= 0:
        x_search -= 1
    return x_search, y

def find_adjacent_number(M, x, y):
    numbers = []
    locations = [1, 0, -1]
    for yd in locations:
        for xd in locations:
            xs, ys = x + xd, y + yd
            if 0 <= xs < M.shape[1] and 0 <= ys < M.shape[0]:
                if M[ys, xs] >= 0:
                    while xs > 0 and M[ys, xs-1] >= 0:
                        xs -= 1
                    numbers.append((xs, ys))
                    if (xs-x) <= 0:
                        # If we have reach past 0 (or more left), there won't be anything left to read on x
                        break
    return numbers

# Recursive function
# If there's a number on the left, go to it
def complete_number(M : np.array, x, y, number = 0):
    number = number * 10 + M[y, x]
    # Read mode
    x_search = x + 1
    if x_search < M.shape[1]:
        # In the matrix
        if M[y, x_search] >= 0:
            # Continue reading
            number = complete_number(M, x_search, y, number)
    return number

def valid_gear_ratios(data : str) -> list:
    # 1)+2) Create the matrix with replaced values
    gear_ratios = []
    lines = data.split(LINE_DELIMITER)
    M = np.array([[number_match(x) for x in list(l)] for l in lines])
    gear_positions = np.where(M == GEAR_NUMBER)
    numbers_start_cache = []
    for (y, x) in zip(*gear_positions):
        adjacent_numbers = find_adjacent_number(M, x, y)
        gear = 1
        if len(adjacent_numbers) == 2:
            # Exactly two numbers adjacent to the gear
            for (nx, ny) in adjacent_numbers:
                if (nx, ny) not in numbers_start_cache:
                    numbers_start_cache.append((nx, ny))
                    number = complete_number(M, nx, ny)
                    gear *= number
            gear_ratios.append(gear)
    return gear_ratios

def main():
    file = argv[1]
    with open(file) as f:
        data = f.read()
        numbers = valid_gear_ratios(data)
        print(sum(numbers))


if __name__ == '__main__':
    main()