# Start over
from sys import argv
import re


variables = [
    'seed-to-soil map',
    'soil-to-fertilizer map',
    'fertilizer-to-water map',
    'water-to-light map',
    'light-to-temperature map',
    'temperature-to-humidity map',
    'humidity-to-location map'
]

class Map:
    def __init__(self, dest : int, src : int, length : int) -> None:
        self._dest = dest
        self._src = src
        self._len = length
        self._src_end = self._src + self._len - 1
        self._offset = self._dest - self._src
    
    def __repr__(self) -> str:
        return f'{self._src}:>{self._src_end}:{self._offset:+n}'

    def offset(self):
        return self._offset

    def start(self):
        return self._src

    def end(self):
        return self._src_end

class Range:
    def __init__(self, start : int, length : int = None, end : int = None) -> None:
        self._start = start
        if end is not None:
            self._end = end
            self._length = self._end - self._start + 1 
        elif length is not None:
            self._end = self._start + length - 1
            self._length = length
        else:
            raise RuntimeError("Either end or length must be defined")

    def __repr__(self) -> str:
        return f'{self._start}->{self._end}'

    def start(self):
        return self._start
    
    def end(self):
        return self._end

    def length(self):
        return self._length

    def contains(self, x):
        return self.start() <= x <= self.end()

    def __eq__(self, __o: object) -> bool:
        return __o.start() == self.start() and __o.end() == self.end()

    def apply_maps(self, maps : list) -> list:
        # Apply all maps first
        ranges = []
        source_mapped_ranges = []
        for _map in maps:
            b_start = max(self.start(), _map.start())
            b_end = min(self.end(), _map.end())
            if b_end >= b_start:
                nr = Range(start=b_start+_map.offset(), end=b_end+_map.offset())
                original = Range(start=b_start, end=b_end)
                source_mapped_ranges.append(original)
                ranges.append(nr)

        # Add all the missing ranges
        source_mapped_ranges = reduce(source_mapped_ranges)
        source_mapped_ranges.sort(key=lambda x : x.start())
        
        start = self.start()
        r : Range
        if len(source_mapped_ranges) == 0:
            # Add everything
            ranges.append(self)
        else:
            start = self.start()
            for r in source_mapped_ranges:
                end = r.start() - 1
                if end >= start:
                    # Add this range
                    nr = Range(start=start, end=end)
                    ranges.append(nr)
                start = r.end() + 1
            end = self.end()
            if end >= start:
                nr = Range(start=start, end=end)
                ranges.append(nr)

        ranges.sort(key=lambda x : x.start())

        assert sum([r.length() for r in ranges]) == self.length()

        return ranges

    def overlap(self, range_2) -> bool:
        return self.start() <= range_2.start() <= self.end() or \
            range_2.start() <= self.start() <= range_2.end() 

    def __or__(self, range_2):
        return Range(start=min(self.start(), range_2.start()), end=max(self.end(), range_2.end()))


def reduce(ranges : list) -> list:
    r1 : Range
    r2 : Range

    new_ranges = []
    exclude = []
    for i1, r1 in enumerate(ranges):
        if i1 in exclude:
            continue
        new_range = r1
        for i2, r2 in enumerate(ranges):
            if new_range.overlap(r2):
                new_range |= r2
                exclude.append(i2)
        new_ranges.append(new_range)
    return new_ranges

def parse_categories(data):
    pattern = '(?:([\w -]+):[ \n])([\d\n ]+)'
    categories = re.findall(pattern, data)
    return {name : [[int(x) for x in line.split(' ') if x != ''] for line in values.split('\n') if line != ''] for name, values in categories}


def seed_ranges(seeds : list) -> list:
    return [Range(start=s, length=l) for s, l in zip(seeds[::2], seeds[1::2])]


def apply_maps_to_ranges(maps : list, ranges : list):
    new_ranges = []
    # Apply maps to each range
    _range : Range
    for _range in ranges:
        new_ranges += _range.apply_maps(maps)
    #print(f'Ranges after map (unreduced) : {new_ranges}')
    #new_ranges = reduce(new_ranges)
    #print(f'Ranges after map : {new_ranges}')
    return new_ranges


def main():
    file = argv[1]
    with open(file) as f:
        data = f.read()
        categories = parse_categories(data)
        seeds = seed_ranges(categories['seeds'][0])
        maps = [[Map(*m) for m in categories[v]] for v in variables]

        ranges = seeds
        for _map in maps:
            # V is the source variable
            ranges = apply_maps_to_ranges(_map, ranges)

        

        #print(min([r.start() for r in ranges]))





if __name__ == '__main__':
    main()