import sys
import enum
from typing import Any

# 12668 : too high
# 11504 : false

class Shape(enum.IntEnum):
    ROCK = 1
    PAPER = 2
    SCISSOR = 3

MATCH = {
    'A' : Shape.ROCK,
    'B' : Shape.PAPER,
    'C' : Shape.SCISSOR,
    'X' : Shape.ROCK,
    'Y' : Shape.PAPER,
    'Z' : Shape.SCISSOR
}

class Result(enum.IntEnum):
    LOSS = 0
    TIE = 3
    WIN = 6

class Run:
    def __init__(self, theirs : Shape, mine : Shape) -> None:
        self.theirs = theirs
        self.mine = mine

    @staticmethod
    def from_string(string : str):
        return Run(*[MATCH[x] for x in string.split(' ')])

    def result(self) -> Result:
        d = self.mine - self.theirs
        r = int(-1/2*d**3 + 3/2*d)
        if r == 0:
            return Result.TIE
        elif r > 0:
            return Result.WIN
        else:
            return Result.LOSS

    def __str__(self) -> str:
        return f"{self.theirs.name} {self.mine.name}"
        

def main():
    file = sys.argv[1]
    with open(file) as f:
        data = f.read()

    runs = [Run.from_string(line) for line in data.split('\n')]

    total = 0

    for run in runs:
        total += run.result()
        total += run.mine

    print(f'Total : {total}')

if __name__ == '__main__':
    main()
