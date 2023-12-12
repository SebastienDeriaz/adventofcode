from sys import argv


BROKEN = '#'
UNKNOWN = '?'
OPERATIONAL = '.'



def parse_line(line : str):
    conditions, counts = line.split(' ')
    counts = [int(x) for x in counts.split(',')]
    return conditions, counts

def unfold(conditions, counts, unfold_factor):
    new_conditions = '?'.join([conditions]*unfold_factor)
    new_counts = counts * unfold_factor
    return new_conditions, new_counts



def count_conditions(conditions):
    return [len(x) for x in conditions.split(OPERATIONAL) if x != '']

def arangements(conditions : str, counts : list):
    # Try out all possibilities
    N = 0
    N_unknowns = conditions.count(UNKNOWN)
    for i in range(0, 2**N_unknowns):
        bits = [int(x) for x in f'{i:0{N_unknowns}b}']
        b_counter = 0
        new_conditions = ''
        for i, c in enumerate(conditions):
            if c == UNKNOWN:
                if bits[b_counter]:
                    new_conditions += OPERATIONAL
                else:
                    new_conditions += BROKEN
                b_counter += 1
            else:
                new_conditions += c

        if count_conditions(new_conditions) == counts:
            N += 1
    return N

UNFOLD_FACTOR = 5

def main():
    file = argv[1]
    with open(file) as f:
        lines = f.readlines()
        N = 0
        for line in lines:
            parsed_line = parse_line(line)
            parsed_line = unfold(*parsed_line, UNFOLD_FACTOR)
            print(parsed_line)
            n = arangements(*parsed_line)
            print(f' -> {n}')
            N += n
        print(f'Total : {N}')
        #conditions_counts = [parse_line(line) for line in lines if line != '']
        #print(conditions_counts)

if __name__ == '__main__':
    main()