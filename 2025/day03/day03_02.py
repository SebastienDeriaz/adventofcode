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

    # number of batteries
    N = 12
    total_power = 0

    for bank in batteries:
        l = -1
        power = 0
        L = len(bank)
        #print(bank)
        for n in range(N, 0, -1):
            sub_bank = bank[l+1:L-n+1]
            _max = max(sub_bank)
            new_l = sub_bank.index(_max) + (l+1 if l >= 0 else 0)
            #print(" " + "".join(str(x) for x in sub_bank) + f' -> {_max}@{new_l}')
            l = new_l
            power += _max * 10**(n-1)

        #print(f'{"".join(str(x) for x in bank)} : {power}')

        total_power += power

    print(total_power)



    
    return

    for bank in batteries:
        bank: list[int]
        # Find the maximum (ignore the last one)
        # Find its location (the most on the left if multiple)
        _max_units = max(bank[l+1:])

        power = _max_tens * 10 + _max_units


        total_power += power


                




if __name__ == '__main__':
    main()