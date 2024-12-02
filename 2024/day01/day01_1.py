import sys
import re

def main():
    file = sys.argv[1]

    with open(file) as f:
        data = f.read()
        
        A = []
        B = []

        for x in data.split('\n'):
            if x:
                a, b = re.match('(\d+) +(\d+)', x).groups()
                A.append(int(a))
                B.append(int(b))

        A.sort()
        B.sort()

        print(sum(abs(a - b) for a, b in zip(A, B)))

if __name__ == '__main__':
    main()