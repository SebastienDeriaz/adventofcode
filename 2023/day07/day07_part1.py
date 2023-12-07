from enum import Enum
from collections import Counter
from sys import argv

N_CARDS_PER_HAND = 5
cards = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']

class HandType(Enum):
    HIGH_CARD = 0
    ONE_PAIR = 1
    TWO_PAIR = 2
    THREE_OF_A_KIND = 3
    FULL_HOUSE = 4
    FOUR_OF_A_KIND = 5
    FIVE_OF_A_KIND = 6

N = max([len(cards), len(HandType)])

# is card[4] + card[3]*len(cards) + ... + card[0]*len(cards)**4 + hand_kind**len(cards)**5

def kind(descriptor) -> HandType:
    matches = {
        (5,) : HandType.FIVE_OF_A_KIND,
        (1, 4) : HandType.FOUR_OF_A_KIND,
        (2, 3) : HandType.FULL_HOUSE,
        (1, 1, 3) : HandType.THREE_OF_A_KIND,
        (1, 2, 2) : HandType.TWO_PAIR,
        (1, 1, 1, 2) : HandType.ONE_PAIR,
        (1, 1, 1, 1, 1) : HandType.HIGH_CARD
    }
    groups_sizes = tuple(sorted(Counter(descriptor).values()))
    return matches[groups_sizes]

class Hand:
    def __init__(self, descriptor, bid) -> None:
        assert len(descriptor) == N_CARDS_PER_HAND
        self._score = 0
        # Calculate cards score
        for i, d in enumerate(descriptor):
            if i > 0:
                self._score *= len(cards)
            self._score += cards.index(d)
        # Calculate rank score
        self._score += kind(descriptor).value * len(cards)**5
        self._descriptor = descriptor
        self._bid = bid

    def __repr__(self) -> str:
        return f"{self._descriptor} : {self._score} ({self._bid})"

    def score(self):
        return self._score

    def bid(self):
        return self._bid

def parse_cards(data : str):
    cards = []
    for line in data.split('\n'):
        if line != '':
            descriptor, bid = line.split(' ')
            cards.append(Hand(descriptor, int(bid)))
    return cards


def main():
    file = argv[1]
    with open(file) as f:
        data = f.read()
        unsorted_cards = parse_cards(data)
        cards = sorted(unsorted_cards, key=lambda x : x.score())
        winnings = [c.bid() * (r+1) for r, c in enumerate(cards)]
        print(sum(winnings))


if __name__ == '__main__':
    main()
        
        
