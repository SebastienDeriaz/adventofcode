# No need to create dictionaries, a simple start + offset will do
# if the value is >= start, add offset, otherwise keep it
# There can be multiple ranges
from sys import argv
import re

# Each variables[x] can be mapped to variables[x+1]
variables = [
    'seed',
    'soil',
    'fertilizer',
    'water',
    'light',
    'temperature',
    'humidity',
    'location'
]


def parse_maps(data):
    pattern = '(\w+)-to-(\w+) map:\n((?:[\w ]+\n)+)'
    # Map from x to the next one
    maps = {}
    for a, b, _maps in re.findall(pattern, data):
        map_blocks = [[int(y) for y in x.split(' ') if y != ''] for x in _maps.split('\n') if x != '']
        maps[a] = map_blocks
    return maps


def parse_seeds(data):
    # Return the list of seeds
    pattern = 'seeds:([ \w]+)'
    seeds_str = re.match(pattern, data).groups()
    seeds = [int(x) for x in seeds_str[0].split(' ') if x != '']
    return seeds

def map_x_to_y(maps, x_values, x, y):
    xi = variables.index(x)
    yi = variables.index(y)
    values = x_values
    for i in range(xi, yi):
        map_key = variables[i]
        for vi, v in enumerate(values):
            map_blocks = maps[map_key]
            for _map in map_blocks:
                if _map[1] <= v <= _map[1] + _map[2]:
                    # The value is contained in the map
                    # Convert it
                    values[vi] += _map[0] - _map[1]
            print(f"{map_key} {v} -> {values[vi]}")
    return values



def main():
    file = argv[1]
    with open(file) as f:
        data = f.read()

        seeds = parse_seeds(data)
        maps = parse_maps(data)
        locations = map_x_to_y(maps, [82], 'seed', 'location')
        print(min(locations))


if __name__ == '__main__':
    main()