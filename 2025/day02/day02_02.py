from sys import argv
from math import log10, floor


# n=2 : 123123 1212 1010 ...
# n=3 : 121212 130130130 100100100 ...
# n=4 : 10101010 1111 123123123123 ...
# .
# .


# Loop over each range (n=2)
#   Find the smallest n-number
#   Find the biggest n-number
#   Remove them and count inbetween
#   Repeat for n+1 until it is not valid anymore ()

# 48778610162 too high


def to_mn(x : int, n : int):
    return int(str(x)*n)

def _l_base_leads(x : int, n : int):
    s = str(x)
    L = len(s)

    size = L // n
    if L % n != 0:
        base = None
        leads = []
    else:
        base = int(s[:size])
        leads = []
        for i in range(L // size):
            if i == 0:
                continue
            leads.append(
                int(s[size*i:size*(i+1)])
            )

    return L, base, leads

def smaller_or_equal_mn(x : int, n : int):
    L, base, leads = _l_base_leads(x, n)

    if base is None:
        return 10**(L//n)-1

    if L == 1:
        return 0
    
    output = base

    for lead in leads:
        if lead > base:
            break
        elif lead == base:
            continue
        else:
            output -= 1
            break

    return output

def bigger_or_equal_mn(x : int, n : int):
    L, base, leads = _l_base_leads(x, n)

    if base is None:
        return 10**(L//n)

    if L == 1:
        return 0

    output = base

    for lead in leads:
        if lead > base:
            output += 1
            break
        elif lead == base:
            continue
        else:
            break

    return output  

def main():
    file = argv[1]
    with open(file, 'r') as f:
        data = f.read()

        ranges = [[int(x) for x in r.split('-')] for r in data.split(',') if r]

        _sum = 0

        for a, b in ranges:
            n = 2
            numbers = []
            while True:
                if n > len(str(b)):
                    break

                low = smaller_or_equal_mn(a-1, n)
                high = bigger_or_equal_mn(b+1, n)

                new_numbers = [to_mn(x, n) for x in range(low+1, high)]

                numbers += new_numbers

                n += 1

            # Remove duplicate 
            numbers = list(set(numbers))
            #print(f'{a}-{b} : {numbers}')
            assert all(num <= b for num in numbers)
            assert all(num >= a for num in numbers)


            _sum += sum(numbers)

    print(_sum)

if __name__ == '__main__':
    main()