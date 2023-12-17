from sys import argv
import numpy as np
from colorama import Style, Fore

def parse_matrix(data):
    return np.array([[int(x) for x in line] for line in data.split('\n') if line != ''])

NEIGHBOURS = [
        (0, 1),
        (0, -1),
        (-1, 0),
        (1, 0)
    ]

def total_heat_losses(heat_loss_matrix):
    positions = [(0,0)]
    total_heat_loss_matrix = np.zeros_like(heat_loss_matrix)
    
    while True:
        new_positions = []
        for x, y in positions:
            # Propagate around this position
            c = total_heat_loss_matrix[y, x]
            for dx, dy in NEIGHBOURS:
                x2, y2 = x + dx, y + dy
                if 0 <= x2 < total_heat_loss_matrix.shape[1] and 0 <= y2 < total_heat_loss_matrix.shape[0] and not (x2 == 0 and y2 == 0):
                    
                    total = c + heat_loss_matrix[y2, x2]
                    if total_heat_loss_matrix[y2, x2] == 0 or total_heat_loss_matrix[y2, x2] > total:
                         total_heat_loss_matrix[y2, x2] = total
                         new_positions.append((x2, y2))
        if len(new_positions) == 0:
            break
        positions = new_positions
    return total_heat_loss_matrix


def least_loss_neighbours(matrix, position):
    x, y = position
    c = matrix[y, x]
    values = []
    for dx, dy in NEIGHBOURS:
        x2, y2 = x + dx, y + dy
        if 0 <= x2 < matrix.shape[1] and 0 <= y2 < matrix.shape[0] and (x2, y2):
            values.append((c - matrix[y2, x2], dx, dy))

    values.sort(key=lambda x : -x[0])

    return [x[1:] for x in values]

def retrace_path(totaled_heat_loss):
    x, y = (totaled_heat_loss.shape[1]-1, totaled_heat_loss.shape[0]-1)
    path = [(x, y)]
    direction_counter = [0, 0]
    while True:
        # Find the direction with the minimal heat loss and no 3x the same direction in a row
        directions = least_loss_neighbours(totaled_heat_loss, (x, y))
        new_direction = None

        if x == 0 and y == 0:
            break

        for dx, dy in directions:
            if (x + dx, y + dy) not in path:
                new_direction = (dx, dy)
                
                if any([abs(dc + k) > 3 for dc, k in zip(direction_counter, new_direction)]):
                    print(f'Exclude ({dx}, {dy})')
                    continue 
                else:
                    if (new_direction[0] == 0) ^ (direction_counter[0] == 0):
                        direction_counter = list(new_direction)
                    else:
                        direction_counter[0] += new_direction[0]
                        direction_counter[1] += new_direction[1]
                    break
        if new_direction is None:
            break
        print(f'Closest to ({totaled_heat_loss[y, x]}) is ({totaled_heat_loss[y + new_direction[1], x+new_direction[0]]})')
        x, y = x + new_direction[0], y + new_direction[1]
        
        path.append((x, y))
    
    return path[::-1]

def print_path(matrix, path):
    for y, line in enumerate(matrix):
        for x, value in enumerate(line):
            if (x, y) in path:
                print(Style.RESET_ALL + Style.BRIGHT + Fore.CYAN, end='')
            else:
                print(Style.RESET_ALL + Style.DIM + Fore.LIGHTBLACK_EX, end='')
            print(value, end='')
        print()

def calculate_heat_loss(matrix, path):
    return sum([matrix[p[1], p[0]] for p in path[1:]])


def main():
    file = argv[1]
    with open(file) as f:
        data = f.read()
        heat_loss_matrix = parse_matrix(data)
        totaled_heat_loss = total_heat_losses(heat_loss_matrix)
        path = retrace_path(totaled_heat_loss)
        print(totaled_heat_loss)
        print_path(heat_loss_matrix, path)
        heat_loss = calculate_heat_loss(heat_loss_matrix, path)
        print(heat_loss)

if __name__ == '__main__':
    main()