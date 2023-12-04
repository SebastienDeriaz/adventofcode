# Recursivity !
# We can start from smallest to biggest
# The goal is to count the number of scratchcards
from sys import argv, stdin
import re


def parse_card(card):
    pattern = 'Card +(\d+):([ \d]+)\|([ \d]+)'
    card_number, winning_numbers, hand_numbers = re.match(pattern, card).groups()
    winning_numbers = [int(x) for x in filter(None, winning_numbers.split(' '))]
    hand_numbers = [int(x) for x in filter(None, hand_numbers.split(' '))]
    card_number = int(card_number)

    _set = set(winning_numbers) & set(hand_numbers)
    matches = len(_set)
    return card_number, matches

def cards_and_matches(data):
    LINE_END = '\n'
    cards = data.split(LINE_END)
    cards_matches = []
    for card in cards:
        card_number, matches = parse_card(card)
        cards_matches.append((card_number, matches))

    return cards_matches

def calculate_cards(cards):
    output = {}
    cards_counter = {card[0] : 1 for card in cards}
    for i, (card_number, matches) in enumerate(cards):
        # Draw the current card N times
        N = cards_counter[card_number]
        output[card_number] = N
        # Add N to all the W next cards (W the amount of matches)
        if matches > 0:
            for i in range(card_number+1, card_number+1+matches):
                cards_counter[i] += N
    return output


def main():
    if len(argv) > 1:
        argument = argv[1]
        if '.' in argument:
            with open(argument) as f:
                data = f.read()
        else:
            data = argument
    else:
        # Read stdin
        data = stdin.read()
    
    cards = cards_and_matches(data)
    result = sum(calculate_cards(cards).values())
    print(result)


if __name__ == '__main__':
    main()