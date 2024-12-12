import sys
import numpy as np
from time import sleep


sys.setrecursionlimit(100000)  # Ewwww, but it works ¯\_(ツ)_/¯

UP = np.array([-1, 0])
DOWN = np.array([1, 0])
LEFT = np.array([0, -1])
RIGHT = np.array([0, 1])

DIRECTIONS = [UP, DOWN, LEFT, RIGHT]



def parse_data(data) -> np.ndarray:
    return np.array([list(line) for line in data.split('\n') if line])

def valid(x, matrix):
    return 0 <= x[0] < matrix.shape[0] and 0 <= x[1] < matrix.shape[1]

def circler(matrix, id_matrix, plots : dict, start):

    for r in range(matrix.shape[0]):
        for c in range(matrix.shape[1]):
            p = (r, c)
        
            p_letter = matrix[tuple(p)]

            


            neighbors = []
            id = None
            for d in DIRECTIONS:
                p2 = p + d
                if not valid(p2, matrix):
                    neighbors.append((None, -1))
                    continue
                else:
                    neighbors.append((p2, matrix[tuple(p2)]))
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

            # Order the neightbors by if they are the same letter or not
            neighbors.sort(key=lambda x : x[1] == p_letter, reverse=True)

def perp_vecs(v):
    vp = np.array([v[1], -v[0]])
    return [vp, -vp]

def side_counter(id_matrix):
    sides = {}
    #print(id_matrix)
    for id in np.unique(id_matrix):
        added_sides = {}
        sides[id] = 0
        #print(f'Processing ID {id}...')
        R, C = np.where(id_matrix == id)
        for r, c in zip(R, C):
            p = np.array([r, c])
            added_sides[tuple(p)] = []
            #print(p)

            for d in DIRECTIONS:
                p2 = p + d
                if valid(p2, id_matrix):
                    # If this neighbor is the same plot, ignore it
                    if id_matrix[tuple(p2)] == id:
                        continue
                
                # Check if any of the perpendicular neighbors have already added this side
                for d2 in perp_vecs(d):
                    p3 = p + d2
                    if valid(p3, id_matrix):
                        if tuple(p3) in added_sides and tuple(d) in added_sides[tuple(p3)]:
                            # This direction already exists, so ignore it
                            break
                else:
                    sides[id] += 1
                added_sides[tuple(p)].append(tuple(d))

    return sides


def circle_plots(matrix):
    id_matrix = np.zeros_like(matrix, dtype=int)
    plots = {}
    # Start the recursive function at the first position
    start = np.array([0, 0])

    circler(matrix, id_matrix, plots, start)

    return id_matrix, plots

def main():
    file = sys.argv[1]
    with open(file) as f:
        data = f.read()

        matrix = parse_data(data)

        id_matrix, plots = circle_plots(matrix)

        sides = side_counter(id_matrix)


        price = 0
        for id in plots:
            price += plots[id][1] * sides[id]

        print(price)


if __name__ == '__main__':
    main()