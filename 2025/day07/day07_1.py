from sys import argv


SPACE = '.'
SPLITTER = '^'
START = 'S'
BEAM = '|'

from colorama import Fore

# 1666 too low
# 1777 too high (assumed)

def main():
    file = argv[1]

    with open(file) as f:
        file_contents = f.read()


        beams = set()


        beam_split = 0

        for line in file_contents.split('\n'):
            if not line:
                continue
            
            #line_string = ''

            new_beams = beams.copy()
            for i, x in enumerate(line):
                if x == START:
                    new_beams.add(i)
                    #line_string += 'S'
                elif x == SPLITTER:
                    if i in beams:
                        new_beams.remove(i)
                        #line_string = line_string[:-1] + BEAM
                        #line_string += f'{Fore.GREEN}{SPLITTER}{Fore.RESET}'
                        beam_split += 1
                        new_beams.add(i-1)
                        new_beams.add(i+1)

                    # else:
                    #     line_string += f'{Fore.RED}{SPLITTER}{Fore.RESET}'

                # elif i in beams or i in new_beams:
                #     line_string += BEAM
                # else:
                #     line_string += SPACE

            beams = new_beams

            #print(line_string)

        print(beam_split)

if __name__ == '__main__':
    main()





            