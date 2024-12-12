import sys
import numpy as np


sys.setrecursionlimit(100000)  # Ewwww, but it works ¯\_(ツ)_/¯

UP = np.array([-1, 0])
DOWN = np.array([1, 0])
LEFT = np.array([0, -1])
RIGHT = np.array([0, 1])

DIRECTIONS = [UP, DOWN, LEFT, RIGHT]



def parse_data(data) -> np.ndarray:
    return np.array([list(line) for line in data.split('\n') if line])

def recursive_circler(matrix, id_matrix, plots : dict, p):
    p_letter = matrix[tuple(p)]
    #print(f'{tuple(p)} : {p_letter}')
    # Look around p, if it touches a valid id_matrix (> 0) and
    # p's matrix value is the same as the valid id_matrix matrix value, then
    # add it to this plot
    # Otherwise, add it to a new plot

    def valid(x):
        return 0 <= x[0] < matrix.shape[0] and 0 <= x[1] < matrix.shape[1]


    neighbors = []
    id = None
    for d in DIRECTIONS:
        p2 = p + d
        if not valid(p2):
            neighbors.append((None, -1))
            continue
        else:
            neighbors.append((p2, matrix[tuple(p2)]))
        #print(f'check {p2} (id {id_matrix[tuple(p2)]}, {matrix[tuple(p2)]})')
        p2_id = id_matrix[tuple(p2)]
        if p2_id > 0:
            if matrix[tuple(p2)] == p_letter:
                if id is not None and p2_id != id:
                    
                    # If a plot already exists and this plot touches the current letter which already has an ID
                    # Merge the two plots and remove the old one
                    plots[id][1] += plots[p2_id][1]
                    plots[id][2] += plots[p2_id][2]
                    plots.pop(p2_id)
                    id_matrix[id_matrix == p2_id] = id
                else:
                    # This p belongs with this plot
                    id = id_matrix[tuple(p2)]

    if id is None:
        # This is a new plot, give it a new number
        if plots == {}:
            id = 1
        else:
            id = max(plots) + 1
    
    id_matrix[tuple(p)] = id

    # Update surface
    if id not in plots:
        plots[id] = [p_letter, 0, 0]
    plots[id][1] += 1

    # Update fences
    n_fences = len(list(filter(lambda x : x[1] != matrix[tuple(p)], neighbors)))
    plots[id][2] += n_fences
    #print(f'{id} ({p_letter}) + {n_fences} fences = {fences[id]}')

    # Order the neightbors by if they are the same letter or not
    neighbors.sort(key=lambda x : x[1] == p_letter, reverse=True)

    # Finally, run the recursive algorithm on the rest
    for i, (p2, letter) in enumerate(neighbors):
        if p2 is not None and id_matrix[tuple(p2)] == 0:
            recursive_circler(matrix, id_matrix, plots, p2)


def circle_plots(matrix):
    id_matrix = np.zeros_like(matrix, dtype=int)
    plots = {}
    # Start the recursive function at the first position
    start = np.array([2, 5])
    recursive_circler(matrix, id_matrix, plots, start)

    return plots

def main():
    file = sys.argv[1]
    with open(file) as f:
        data = f.read()

        matrix = parse_data(data)

        plots = circle_plots(matrix)

        price = 0

        for k, (letter, s, f) in plots.items():
            #print(f'Plot N°{k:<2} ({letter}) : Surface={s} Fences={f}')
            price += f * s
        print(f'Total price : {price}')


if __name__ == '__main__':
    main()