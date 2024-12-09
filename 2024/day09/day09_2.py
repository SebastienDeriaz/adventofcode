import sys


EMPTY = '.'

def parse(data):
    blocks = []
    is_block = True
    position = 0
    id = 0
    for d in data:
        d = int(d)
        if is_block:
            blocks.append((position, d, id))
            id += 1
        position += d

        is_block = not is_block

    return blocks

def compact_memory(blocks : list):
    memory = blocks.copy()
    N = len(memory)
    # Loop over blocks in reverse
    for b in blocks[::-1]:
        #print(f'Place {b[2]}')
        # Find a space for it up to its location
        for i in range(N-1):
            previous = memory[i]
            current = memory[i+1]
            # If there's space, put it
            end_of_previous = previous[0] + previous[1] 
            if end_of_previous > b[0]:
                break
            free_space = current[0] - end_of_previous
            # if current == b:
            #     free_space += b[1]
            #print(f'{previous[2]}-{current[2]} : {free_space}')
            if free_space >= b[1]:
                #print(f' -> {end_of_previous}')
                memory.remove(b)
                memory.insert(i+1, (end_of_previous, b[1], b[2]))
                #print(memory)
                #print(memory_string(memory))
                break

    return memory

def memory_string(blocks):
    string = ''
    position = 0
    for p, l, v in blocks:
        while position < p:
            string += EMPTY
            position += 1
        string += f'{v}'*l
        position += l

    return string

def checksum(memory):
    output = 0
    for block in memory:
        for k in range(block[0], block[0]+block[1]):
            output += k * block[2]

    return output



def main():
    file = sys.argv[1]
    
    with open(file) as f:
        data = f.read()

        blocks = parse(data)

        #print(memory_string(blocks))

        memory = compact_memory(blocks)

        #print(memory_string(memory))

        print(checksum(memory))

        

if __name__ == '__main__':
    main()