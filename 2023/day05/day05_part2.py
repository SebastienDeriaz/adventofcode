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

def apply_map_to_range(_map : Map, _range : Range) -> list:
    # Create a single smaller or equal map
    start = max([_map.start(), _range.start()])
    end = min([_map.end(), _range.end()])
    length = end - start + 1
    if length > 0:
        # There is a range !
        return (Range(start, length), Range(start+_map.offset(), length))


def apply_maps_to_range(maps : list, _range : Range):
    print()
    print(f'Apply {maps} to {_range}')
    map_ranges = []
    maps.sort(key=lambda x : x.start())
    for _map in maps:
        output = apply_map_to_range(_map, _range)
        if output is not None:
            map_ranges.append(output)

    # Add the missing ranges
    start = _range.start()
    output_ranges = []
    original_range = None
    for original_range, mapped_range in sorted(map_ranges, key=lambda x : x[0].start()):
        if original_range.start() > start:
            # Add a non-map range
            output_ranges.append((Range(start, original_range.start() - start), Range(start, original_range.start() - start)))
        # Add the current map range
        output_ranges.append((original_range, mapped_range))
        start = mapped_range.end() + 1
    if original_range is None:
        # No map-range at all, return the original range
        output_ranges.append((_range, _range))
    elif original_range.end() < _range.end():
        # Add the final non-map range
        _rng = Range(original_range.end()+1, _range.end() - original_range.end())
        output_ranges.append((_rng, _rng))

    output = sorted([x[1] for x in output_ranges], key=lambda x : x.start())
    #assert output[0].start() > 0
    return output



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

def apply_maps_to_ranges(maps : list, ranges : list):
    _ranges = []
    for _range in ranges:
        _ranges += apply_maps_to_range(maps, _range)
    return sorted(_ranges, key=lambda x : x.start())
        
def main():
    file = argv[1]
    with open(file) as f:
        data = f.read()
        seeds = parse_seeds(data)
        variable_maps = parse_maps(data)

        ranges = seeds
        #for v in variables[:-1]:
        for v in variables[:-1]:
            print(f"###################### Apply variable {v} ####################################")
            ranges = apply_maps_to_ranges(variable_maps[v], ranges)

        print(ranges)

        #print([x2.start() - x1.start() for x1, x2 in zip(ranges[:-1], ranges[1:])])

        print(ranges[0].start())


if __name__ == '__main__':
    main()