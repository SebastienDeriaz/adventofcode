from sys import argv
from colorama import Fore, Back

SPACE = '.'
SPLITTER = '^'
START = 'S'
BEAM = '|'

COLORS = [
    Fore.RED,
    Fore.YELLOW,
    Fore.WHITE,
    Fore.GREEN,
    Fore.CYAN,
    Fore.BLUE,
    Fore.MAGENTA,
    Fore.LIGHTMAGENTA_EX
]

VALUES_PER_COLOR = 15000000000000

def beam_color(x : int):
    for i, color in enumerate(COLORS):
        limit = VALUES_PER_COLOR * i + 1

        if x <= limit:
            return color
        
    return Back.RED

def main():
    file = argv[1]

    with open(file) as f:
        file_contents = f.read()

        beams = {}

        for line in file_contents.split('\n'):
            if not line:
                continue
            
            new_beams = beams.copy()
            for i, x in enumerate(line):
                # Init the dictionary
                if i not in beams:
                    new_beams[i] = 0

                if x == START:
                    new_beams[i] += 1
                elif x == SPLITTER:
                    if beams[i] > 0:
                        new_beams[i] = 0
                        new_beams[i+1] += beams[i]
                        new_beams[i-1] += beams[i]

            # line_string = ''
            # for i, x in enumerate(line):
            #     if x == START:
            #         line_string += START
            #     elif x == SPLITTER:
            #         if beams[i] > 0:
            #             line_string += f'{Fore.GREEN}{SPLITTER}{Fore.RESET}'
            #         else:
            #             line_string += f'{Fore.RED}{SPLITTER}{Fore.RESET}'
            #     elif new_beams[i] > 0:
            #         line_string += f'{beam_color(new_beams[i])}{BEAM}{Fore.RESET}'
            #     else:
            #         line_string += SPACE
            # print(line_string)

            beams = new_beams


        beam_split = sum(new_beams.values())
        print(beam_split)
        #print()

if __name__ == '__main__':
    main()





            