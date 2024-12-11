import sys



def blink(stones, N):
    new_stones = []
    if N == 0:
        return stones
    else:
        for s in stones:
            if s == 0:
                new_stones.append(1)
            elif len(str(s)) % 2 == 0:
                s_str = str(s)
                left = int(s_str[:len(s_str)//2])
                right = int(s_str[len(s_str)//2:])
                new_stones.append(left)
                new_stones.append(right)
            else:
                new_stones.append(s * 2024)
        new_stones = blink(new_stones, N-1)
    return new_stones

def main():
    file = sys.argv[1]
    
    with open(file) as f:
        data = f.read()
        stones = [int(x) for x in data.split(' ')]

        N = 25
        after_blinks = blink(stones, N)

        print(len(after_blinks))

if __name__ == '__main__':
    main()