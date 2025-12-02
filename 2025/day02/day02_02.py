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


def to_mn(x : int, n : int):
    return int(str(x)*n)

def _l_base_leads(x : int, n : int):
    s = str(x)
    L = len(s)

    size = L // n
    if L == 1:
        base = 0
        leads = [0]
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
    L, base, lead = _l_base_leads(x, n)

    if L == 1:
        return 0
    if L % 2 == 1:
        return 10**(L//2)-1
    
    output = base

    if int(lead) < int(base):
        output -= 1

    return output

def bigger_or_equal_mn(x : int, n : int):
    L, base, lead = _l_base_leads(x, n)

    if L == 1:
        return 0
    if L % 2 == 1:
        return 10**(L//2)

    output = base

    if int(lead) > int(base):
        output += 1

    return output  

def main():
    file = argv[1]
    with open(file, 'r') as f:
        data = f.read()

        ranges = [[int(x) for x in r.split('-')] for r in data.split(',') if r]


        _sum = 0

        for a, b in ranges:
            n = 2
            while True:
                low = smaller_or_equal_mn(a-1, n)
                high = bigger_or_equal_mn(b+1, n)



                print(f'{a}-{b} : ({low})-({high}) n{n} : {numbers}')
                n += 1



            numbers = [to_mn(x) for x in range(low+1, high)]

            _sum += sum(numbers)

    print(_sum)

if __name__ == '__main__':
    main()