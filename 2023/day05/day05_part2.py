# No need to create dictionaries, a simple start + offset will do
# if the value is >= start, add offset, otherwise keep it
# There can be multiple ranges
from sys import argv
import re

class Range:
    def __init__(self, start, length) -> None:
        self._start = start
        self._length = length
        pass

    def __repr__(self) -> str:
        return f"{self._start}->{self._start+self._length-1}"

    def __str__(self) -> str:
        return self.__repr__()

    def start(self):
        return self._start
    
    def end(self):
        return self._start + self._length - 1

class Map:
    def __init__(self, destination, source, length) -> None:
        self._destination = destination
        self._source = source
        self._length = length
        self._offset = self._destination - self._source

    def __repr__(self) -> str:
        return f"{self._source}->{self._source+self._length-1}:{self._offset:+d}"

    def __str__(self) -> str:
        return self.__repr__()

    def start(self):
        return self._source
    
    def end(self):
        return self._source + self._length - 1

def apply_map_to_range(map : Map, range : Range) -> list:
    # Create three new ranges
    # A : smaller than map
    # B : inside map
    # C : bigger than map
    ranges = []
    if range.start() < map.start():
        # A
        start = range.start()
        end = map.start() - 1
        length = end - start + 1
        ranges.append(Range(start, length))
    if map.end() > range.start():
        # B
        start = max(map.start(), range.start())
        end = min(map.end(), range.end())
        length = start - end + 1
        ranges.append(Range(start, length))
    if map.end() < range.end():
        # C
        start = map.end() + 1
        end = range.end()
        length = end - start + 1
        ranges.append(Range(start, length))

    return ranges

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
        map_blocks = [Map(*[int(y) for y in x.split(' ') if y != '']) for x in _maps.split('\n') if x != '']
        maps[a] = map_blocks
    return maps

def parse_seeds(data):
    # Return the list of seeds
    pattern = 'seeds:([ \w]+)'
    seeds_str = re.match(pattern, data).groups()
    seeds_ranges = [int(x) for x in seeds_str[0].split(' ') if x != '']
    seeds = [Range(start, length) for start, length in zip(seeds_ranges[::2], seeds_ranges[1::2])]
    return seeds



# def map_x_to_y(maps, x_ranges, x, y):
#     xi = variables.index(x)
#     yi = variables.index(y)
#     ranges = x_ranges
#     next_ranges = []
#     for i in range(xi, yi):
#         map_key = variables[i]
#         for start, length in ranges:
#             map_blocks = maps[map_key]
#             # Split the current range into multiple smaller ones
#             for rng in ranges:
                

#             for map_destination, map_source, map_length in map_blocks:
#                 # Create this range
#                 # Check if the map source is inside the range
                


#                 sub_range_start = min(map_source, start)

                
#                 if _map[1] <= v <= _map[1] + _map[2]:
#                     # The value is contained in the map
#                     # Convert it
#                     values[vi] += _map[0] - _map[1]
#                     break # It seems like some values overlap
#     return values

def main():
    file = argv[1]
    with open(file) as f:
        data = f.read()
        seeds = parse_seeds(data)
        print(f"Seeds : {seeds}")
        maps = parse_maps(data)
        print(f"Maps : {maps}")
        #locations = map_x_to_y(maps, seeds, 'seed', 'location')
        # print(min(locations))


        # TODO : Implement recursive function to apply all the maps on all the ranges


if __name__ == '__main__':
    main()