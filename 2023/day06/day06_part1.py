from sys import argv
import re
from math import sqrt, floor, ceil
from functools import reduce

K_V = 1

def parse_races(data):
    TIME_KEY = 'Time:'
    DISTANCE_KEY = 'Distance:'
    
    for line in data.split('\n'):
        if len(line) > 0:
            values = [int(x) for x in line.split(':')[1].split(' ') if x != '']
            if TIME_KEY in line:
                # Parse times
                times = values         
            elif DISTANCE_KEY in line:
                # Parse distances
                distances = values
    return times, distances
    

def distance_travelled(T, t_b):
    v0 = K_V * t_b
    return (T-t_b)*v0

def roots(T, d_g, k_v):
        x = sqrt(T**2 - 4*d_g/k_v)
        return (T - x)/2, (T + x)/2

def find_button_times(times, distances):
    n_ways = []
    for T, d_g in zip(times, distances):
        t_b_1, t_b_2 = roots(T, d_g, K_V)
        print(T, d_g, t_b_1, t_b_2)
        N = int(floor(t_b_2) - ceil(t_b_1) + 1)
        n_ways.append(N)
        print(f"{T}ms {d_g}mm -> {N}")
    return n_ways


def main():
    file = argv[1]
    with open(file) as f:
        data = f.read()
        times, distances = parse_races(data)
        ways = find_button_times(times, distances)
        print(ways)

        N = reduce(lambda a, b : a * b, ways)

        print(N)





if __name__ == '__main__':
    main()