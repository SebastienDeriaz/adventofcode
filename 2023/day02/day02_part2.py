# All games are independant, process them one at a time
# Each "subset" can have 1, 2 or 3 colors and any amount of cubes for each
# Each subset is independant from another
# All the subset have to be "valid" for the game to be valid
# A subset is valid if there aren't any more cube drawn as there are available (for each color)
from sys import argv, stdin
from enum import Enum
import re
from functools import reduce

class Colors(Enum):
    RED = 0
    GREEN = 1
    BLUE = 2

COLOR_NAMES = {
    'red' : Colors.RED,
    'green' : Colors.GREEN,
    'blue' : Colors.BLUE,
}

BAG_CONTENTS = {
    Colors.RED : 12,
    Colors.GREEN : 13,
    Colors.BLUE : 14
}

SUBSET_DELIMITER = ';'
COLOR_DELIMITER = ','


def process_game(data):
    # Find the game number and the subsets
    game_pattern = 'Game (\d+):([ \d\w,;]+)'
    n_color_pattern = '[ ]*(\d+)[ ]+(\w+)'

    game_number, subsets = re.match(game_pattern, data).groups()
    game_number = int(game_number)

    colors = {c : 0 for c in Colors}

    # Split the subsets
    for s in subsets.split(SUBSET_DELIMITER):
        # Split each n-color
        for c in s.split(COLOR_DELIMITER):
            # Analyze each n-color
            n, color = re.match(n_color_pattern, c).groups()
            # Update the max number
            colors[COLOR_NAMES[color]] = max(colors[COLOR_NAMES[color]], int(n))

    return game_number, colors


def valid_games(data : str, bag_contents : dict):
    LINE_END = '\n'
    games = []
    for line in data.split(LINE_END):
        game_number, colors = process_game(line)
        # Calculate the power
        power = reduce(lambda a, b : a*b, colors.values())
        games.append((game_number, power))
    return games





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
    
    result = sum([x[1] for x in valid_games(data, BAG_CONTENTS)])
    print(result)

if __name__ == '__main__':
    main()