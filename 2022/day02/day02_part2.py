import sys
from enum import IntEnum, StrEnum

class Shape(StrEnum):
    ROCK = 'A'
    PAPER = 'B'
    SCISSORS = 'C'

class Result(StrEnum):
    LOSS = 'X'
    TIE = 'Y'
    WIN = 'Z'

SCORES = {
    Shape.ROCK : 1,
    Shape.PAPER : 2,
    Shape.SCISSORS : 3,
    Result.LOSS : 0,
    Result.TIE : 3,
    Result.WIN : 6
}

def mine_from_theirs(theirs : Shape, result : Result):
    shapes = list(Shape)
    ti = shapes.index(theirs)
    if result == Result.TIE:
        return theirs
    elif result == Result.WIN:
        return shapes[(ti + 1) % len(shapes)]
    else:
        return shapes[(ti - 1) % len(shapes)]


def main():
    file = sys.argv[1]    
    with open(file) as f:
        data = f.read()

    
    runs = [[Shape(line[0]), Result(line[1])] for line in [line.split(' ') for line in data.split('\n')]]

    total = 0
    for theirs, result in runs:
        mine = mine_from_theirs(theirs, result)
        total += SCORES[result]
        total += SCORES[mine]


    print(f"Total : {total}")


if __name__ == '__main__':
    main()