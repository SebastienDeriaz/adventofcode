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

    def offset(self):
        return self._offset

def apply_map_to_range(map : Map, _range : Range) -> list:
    # Create three new ranges
    # A : smaller than map
    # B : inside map
    # C : bigger than map
    ranges = [_range] # Initial x->x range
    if _range.start() < map.start():
        # A exists
        start = _range.start()
        end = min([_range.end(), map.start() - 1])
        length = end - start + 1
        assert length > 0
        rng = Range(start, length)
        ranges.append(rng)
        print(f"A : {rng}")

    if map.end() >= _range.start() and map.start() <= _range.end():
        # B
        start = max(map.start(), _range.start())
        end = min(map.end(), _range.end())
        length = end - start + 1
        assert length > 0
        rng = Range(start+map.offset(), length)
        ranges.append(rng)
        print(f"B : {rng}")
        
    if map.end() < _range.end() and map.start() >= map.end():
        # C
        start = map.end() + 1
        end = _range.end()
        length = end - start + 1
        assert length > 0
        rng = Range(start, length)
        ranges.append(rng)
        print(f"C : {rng}")

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
    for a, _, _maps in re.findall(pattern, data):
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

def apply_map_to_ranges(map : list, ranges : list):
    ranges_out = []
    for rng in ranges:
        ranges_out += apply_map_to_range(map, rng)
    return ranges_out

def apply_maps_to_seeds(maps, seeds):
    ranges = seeds
    for v in variables[:-1]:
        print(f"Input range : {ranges}")
        new_ranges = []
        _maps = maps[v]
        for _map in _maps:
            print(f"Apply map : {_map}")
            output = apply_map_to_ranges(_map, ranges)
            new_ranges += output
        
        ranges = new_ranges
        print(f"Ranges after {v}-to-x : {ranges}")
    return ranges
        
def main():
    file = argv[1]
    with open(file) as f:
        data = f.read()
        seeds = parse_seeds(data)
        maps = parse_maps(data)
        #print(f"Maps : {maps}")
        locations = apply_maps_to_seeds(maps, seeds)
        print(locations)
        print(min([l.start() for l in locations]))


if __name__ == '__main__':
    main()