from sys import argv, stdin
import re


def parse_card(card):
    pattern = 'Card +(\d+):([ \d]+)\|([ \d]+)'
    print(card)
    card_number, winning_numbers, hand_numbers = re.match(pattern, card).groups()
    winning_numbers = [int(x) for x in filter(None, winning_numbers.split(' '))]
    hand_numbers = [int(x) for x in filter(None, hand_numbers.split(' '))]
    card_number = int(card_number)

    _set = set(winning_numbers) & set(hand_numbers)
    if len(_set) > 0:
        points = 2**(len(_set) - 1)
    else:
        points = 0
    return card_number, points

def cards_points(data):
    LINE_END = '\n'
    cards = data.split(LINE_END)
    points_list = []
    for card in cards:
        card_number, points = parse_card(card)
        points_list.append(points)

    return points_list







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
    
    result = sum(cards_points(data))
    print(result)

if __name__ == '__main__':
    main()