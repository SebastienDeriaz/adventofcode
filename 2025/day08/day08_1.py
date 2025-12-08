from sys import argv
from typing import Dict
import numpy as np
import time
from collections import Counter

def pair(a : int, b : int):
    return f'{a}-{b}'

def main():
    file = argv[1]
    N = int(argv[2])

    positions = []
    with open(file) as f:
        file_contents = f.read()

        for line in file_contents.split('\n'):
            positions.append(tuple(int(x) for x in line.split(',')))

    positions = np.array(positions)

    #print(positions)
    distance_pairs = []
    #distance_pairs_match = {}
    pairs = []

    start = time.time()
    for i, p in enumerate(positions):
        distances = np.linalg.norm(positions - p, axis=1)
        distances[i] = float('inf')
        shortest = int(np.where(distances == distances.min())[0][0])

        pa = pair(i, shortest)
        if (pa not in pairs) and (pair(shortest, i) not in pairs):
            
            pairs.append(pa)
            distance_pairs.append((i, shortest, float(distances.min())))

        # if (shortest in distance_pairs_match) and (distance_pairs[distance_pairs_match[shortest]][1] == i):
        #     distance_pairs_match[i] = distance_pairs[distance_pairs_match[shortest]][1]
        # else:
        #     distance_pairs_match[i] = len(distance_pairs)-1
        #distance_pairs_match[shortest] = len(distance_pairs)-1
        #    print(f'add {pa}')
        #else:
            #print(f'skip {positions[i]} <--> {positions[shortest]}')
    stop = time.time()
    #print(f'Time : {stop-start:.3f}')

    distance_pairs.sort(key=lambda x : x[2])

    # for i, (a, b, distance) in enumerate(distance_pairs):
    #     print(f'{positions[a]} <--> {positions[b]} ({distance:.1f})')
    #     if i == 10:
    #         break
    # return

    #print(len(distance_pairs))

    #circuits = {i : None for i in range(positions.shape[0])}

    current_circuit_id = 0
    connections_count = 0

    circuits : Dict[int, set[int]]= {}

    def circuit_id(x : int):
        for circuit_id, s in circuits.items():
            if x in s:
                return circuit_id
        return None

    current_new_id = 0
    for a, b, distance in distance_pairs:
        a_id = circuit_id(a)
        b_id = circuit_id(b)

        if a_id is not None and b_id is not None:
            # Move everything to a
            circuits[a_id] |= circuits[b_id]
            circuits.pop(b_id)
            id = a_id
        else:
            if a_id is not None:
                id = a_id
            elif b_id is not None:
                id = b_id
            else:
                id = current_new_id
                current_new_id += 1
            
            if id not in circuits:
                circuits[id] = set()
            circuits[id].add(a)
            circuits[id].add(b)

        # if circuits[a] is not None:
        #     circuit_id = circuits[a]
        # elif circuits[b] is not None:
        #     circuit_id = circuits[b]
        # else:
        #     circuit_id = current_circuit_id
        #     current_circuit_id += 1

        # circuits[a] = circuit_id
        # circuits[b] = circuit_id

        print(f'{positions[a, :]} <--> {positions[b, :]} ({id})')

        connections_count += 1
        if connections_count == N:
            break


    # circuit_sizes = {}
    # for circuit in circuits.values():
    #     if circuit is not None:
    #         if circuit not in circuit_sizes:
    #             circuit_sizes[circuit] = 0
    #         circuit_sizes[circuit] += 1

    # print(circuit_sizes.values())

    print(circuits)




if __name__ == '__main__':
    main()