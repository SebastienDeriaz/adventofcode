from sys import argv
from typing import Dict
import numpy as np
import time

def main():
    file = argv[1]
    N_connections = int(argv[2])
    N_largest = int(argv[3])

    positions = []
    with open(file) as f:
        file_contents = f.read()

        for line in file_contents.split('\n'):
            positions.append(tuple(int(x) for x in line.split(',')))

    positions = np.array(positions)

    pairs = []

    k = np.arange(positions.shape[0], dtype=int)

    #start = time.time()
    for a, p in enumerate(positions):
        distances = np.linalg.norm(positions[a+1:,:] - p, axis=1)
        ki = k[a+1:]
        #distances[i] = float('inf')

        pairs += [(a, int(b), d) for b, d in zip(ki, distances)]
    #stop = time.time()
    #print(f'Time : {stop-start:.3f}')

    pairs.sort(key=lambda x : x[2])

    connections_count = 0

    circuits : Dict[int, set[int]]= {}

    def circuit_id(x : int):
        for circuit_id, s in circuits.items():
            if x in s:
                return circuit_id
        return None

    current_new_id = 0
    for a, b, distance in pairs:
        a_id = circuit_id(a)
        b_id = circuit_id(b)

        if a_id is not None and b_id is not None:
            # Move everything to a
            if a_id != b_id:
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

        #print(f'{positions[a, :]} <--> {positions[b, :]} ({id})')

        connections_count += 1
        if connections_count == N_connections:
            break
    
    #print(circuits)

    circuit_lengths = [len(lamps) for lamps in circuits.values()]
    circuit_lengths.sort(reverse=True)

    print(np.prod(circuit_lengths[:N_largest]))




if __name__ == '__main__':
    main()