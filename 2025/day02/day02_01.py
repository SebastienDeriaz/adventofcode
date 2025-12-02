from sys import argv
from math import log10, floor


# Loop over each range
#   Find the smallest double-number
#   Find the biggest double-number
#   Remove them and count inbetween


# smaller or equal dn
#              base lead 
# 341012531 -> 3410-1253-1 -> 3410-1253 -> 3409-3409 -> 3409

# bigger or equal dn
# 341012531 -> 3410-1253-1 -> 3410-1253 -> 3410-3410 -> 3410

def to_dn(x : int):
    return int(f'{x}{x}')

def _l_base_lead(x : int):
    s = str(x)
    L = len(s)
    if L == 1:
        base = 0
        lead = 0
    else:
        base = int(s[:L//2])
        lead = int(s[L//2:L//2*2])

    return L, base, lead

def smaller_or_equal_dn(x : int):
    L, base, lead = _l_base_lead(x)

    if L == 1:
        return 0
    if L % 2 == 1:
        return 10**(L//2)-1
    
    output = base

    if int(lead) < int(base):
        output -= 1

    return output

def bigger_or_equal_dn(x : int):
    L, base, lead = _l_base_lead(x)

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
            low = smaller_or_equal_dn(a-1)
            high = bigger_or_equal_dn(b+1)

            numbers = [to_dn(x) for x in range(low+1, high)]
            #print(f'{a}-{b} : ({low})-({high}) {numbers}')

            _sum += sum(numbers)

    print(_sum)
    #print(ranges)

if __name__ == '__main__':
    main()