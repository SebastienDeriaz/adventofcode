import sys

def parse_data(data):
    return [int(x) for x in data.split('\n')]


def mix(secret_number, new_number):
    return secret_number ^ new_number

def prune(new_number):
    return new_number % 16777216

def price_sequence(secret_number, N):
    number = secret_number
    yield secret_number, secret_number % 10
    for _ in range(N):
        number = prune(mix(number, number * 64))
        number = prune(mix(number, number // 32))
        number = prune(mix(number, number * 2048))
        yield number, number % 10

def main():
    file = sys.argv[1]
    with open(file) as f:
        data = f.read()
        codes = parse_data(data)
        N = 2000

        sellers = [[x[1] for x in price_sequence(code, N)] for code in codes]



        # Find all sequences in sellers
        sequences = {}
        for seller in sellers:
            sequence = []
            this_seller_sequences = {}
            previous = seller[0]
            for p in seller[1:]:
                if len(sequence) == 4:
                    sequence = sequence[1:]
                sequence.append(p - previous)
                previous = p

                if len(sequence) == 4:
                    sequence_tuple = tuple(sequence)
                    if sequence_tuple not in this_seller_sequences:
                        this_seller_sequences[sequence_tuple] = p

            # Add all of the sequences
            for sequence, price in this_seller_sequences.items():
                if sequence in sequences:
                    sequences[sequence] += price
                else:
                    sequences[sequence] = price


        sequence_total = list(sequences.items())
        sequence_total.sort(key=lambda x : x[1], reverse=True)

        print(sequence_total[0][1])

if __name__ == '__main__':
    main()