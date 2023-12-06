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
            value = int(line.split(':')[1].replace(' ', ''))
            if TIME_KEY in line:
                # Parse times
                time = value         
            elif DISTANCE_KEY in line:
                # Parse distances
                distance = value
    return time, distance
    

def distance_travelled(T, t_b):
    v0 = K_V * t_b
    return (T-t_b)*v0

def roots(T, d_g, k_v):
        x = sqrt(T**2 - 4*d_g/k_v)
        return (T - x)/2, (T + x)/2

def find_button_times(T, d_g):
    t_b_1, t_b_2 = roots(T, d_g, K_V)
    print(T, d_g, t_b_1, t_b_2)
    n_ways = int(floor(t_b_2) - ceil(t_b_1) + 1)
    return n_ways


def main():
    file = argv[1]
    with open(file) as f:
        data = f.read()
        times, distances = parse_races(data)
        N = find_button_times(times, distances)
        print(N)





if __name__ == '__main__':
    main()