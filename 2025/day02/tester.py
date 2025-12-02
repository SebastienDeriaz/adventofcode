from sys import argv

from day02_02 import smaller_or_equal_mn, bigger_or_equal_mn, to_mn, _l_base_leads

def main():
    a = int(argv[1])
    b = int(argv[2])
    n = int(argv[3])

    # print(f'smaller : {smaller_or_equal_dn(number)}')
    # print(f'bigger : {bigger_or_equal_dn(number)}')
    
    print(f'a={a} : {_l_base_leads(a-1, n)}')
    print(f'b={b} : {_l_base_leads(b+1, n)}')

    _sum = 0
    
    low = smaller_or_equal_mn(a-1, n)
    high = bigger_or_equal_mn(b+1, n)

    numbers = [to_mn(x, n) for x in range(low+1, high)]
    #print(f'{a}-{b} : ({low})-({high}) {numbers}')

    _sum += sum(numbers)

    print(f'{a}-{b} : ({low})-({high}) n{n} : {numbers} => {_sum}')



if __name__ == '__main__':
    main()
