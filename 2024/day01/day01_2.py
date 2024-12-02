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

        score = 0
        for a in A:
            score += a * B.count(a)

        print(score)

if __name__ == '__main__':
    main()