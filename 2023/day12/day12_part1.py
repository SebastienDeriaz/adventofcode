from sys import argv


BROKEN = '#'
UNKNOWN = '?'
OPERATIONAL = '.'



def parse_line(line : str):
    conditions, counts = line.split(' ')
    counts = [int(x) for x in counts.split(',')]
    return conditions, counts


def count_conditions(conditions):
    return [len(x) for x in conditions.split(OPERATIONAL) if x != '']

def arangements(conditions : str, counts : list):
    # First split in groups
    print(f'Line : {conditions}, {counts}')
    # Try out all possibilities
    N = 0
    N_unknowns = conditions.count(UNKNOWN)
    for i in range(0, 2**N_unknowns):
        bits = [int(x) for x in f'{i:0{N_unknowns}b}']
        b_counter = 0
        new_conditions = ''
        for i, c in conditions:
            
            new_conditions += str(y)

            new_conditions = ''.join([(OPERATIONAL if b > 0 else BROKEN) if conditions[i] == UNKNOWN else c  for i, c in enumerate(conditions)])

        print(f'{new_conditions} : {count_conditions(new_conditions)}')
        if count_conditions(new_conditions) == counts:
            print(f'  add')
            N += 1

    print(f'  ->{N}')
    return N



    





def main():
    file = argv[1]
    with open(file) as f:
        lines = f.readlines()
        parsed_line = parse_line(lines[0])
        arangements(*parsed_line)

        #conditions_counts = [parse_line(line) for line in lines if line != '']
        #print(conditions_counts)

if __name__ == '__main__':
    main()