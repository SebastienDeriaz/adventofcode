from sys import argv

def main():
    file = argv[1]

    batteries = []
    with open(file) as f:
        data = f.read()

        for line in data.split('\n'):
            if not line:
                continue
        
            batteries.append([int(x) for x in line])

    
    total_power = 0

    for bank in batteries:
        bank: list[int]
        # Find the maximum (ignore the last one)
        _max_tens = max(bank[:-1])
        # Find its location (the most on the left if multiple)
        l = bank.index(_max_tens)
        _max_units = max(bank[l+1:])

        power = _max_tens * 10 + _max_units


        total_power += power

    print(total_power)

                




if __name__ == '__main__':
    main()