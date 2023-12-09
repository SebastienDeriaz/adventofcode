from sys import argv


def parse_sequences(data : list) -> list:
    return [[int(x) for x in l.split(' ') if x != ''] for l in data]


def find_next_value(sequence):
    # Iterate over all sequences and create the pseudo-triangle 
    sequences = [sequence]
    while any([n != 0 for n in sequences[-1]]):
        sequences.append([x1 - x0 for x0, x1 in zip(sequences[-1][:-1], sequences[-1][1:])])

    # Add a new value to each row
    previous_value = 0
    for i, s in enumerate(sequences[::-1]):
        new_value = previous_value + s[-1]
        s.append(previous_value + s[-1])
        previous_value = new_value
    
    #print(f"New sequence : {sequences[0]}")

    return sequences[0][-1]
            

def main():
    file = argv[1]

    with open(file) as f:
        data = f.readlines()
        sequences = parse_sequences(data)   

        print(sum([find_next_value(sequence) for sequence in sequences]))


if __name__ == '__main__':
    main()
        
