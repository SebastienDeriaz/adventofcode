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
    seeds_ranges = [int(x) for x in seeds_str[0].split(' ') if x != '']
    seeds = [(start, length) for start, length in zip(seeds_ranges[::2], seeds_ranges[1::2])]
    return seeds




def subrange(rng, maps):
    rng_start, rng_length = rng
    ranges = []
    for map_destination, map_source, map_length in maps:
        if map_source + map_length - 1 <= rng_start and rng_start + rng_length - 1 >= map_source:
            # map range is inside the original range
            subrange_start = max(rng_start, map_source)
            subrange_length = 
            
            
        








def map_x_to_y(maps, x_ranges, x, y):
    xi = variables.index(x)
    yi = variables.index(y)
    ranges = x_ranges
    next_ranges = []
    for i in range(xi, yi):
        map_key = variables[i]
        for start, length in ranges:
            map_blocks = maps[map_key]
            # Split the current range into multiple smaller ones
            for rng in ranges:
                

            for map_destination, map_source, map_length in map_blocks:
                # Create this range
                # Check if the map source is inside the range
                


                sub_range_start = min(map_source, start)

                
                if _map[1] <= v <= _map[1] + _map[2]:
                    # The value is contained in the map
                    # Convert it
                    values[vi] += _map[0] - _map[1]
                    break # It seems like some values overlap
    return values



def main():
    file = argv[1]
    with open(file) as f:
        data = f.read()
        seeds = parse_seeds(data)
        print(seeds)
        maps = parse_maps(data)
        locations = map_x_to_y(maps, seeds, 'seed', 'location')
        # print(min(locations))


if __name__ == '__main__':
    main()