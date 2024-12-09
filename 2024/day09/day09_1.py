import sys


EMPTY = '.'

def parse(data):
    blocks = []
    is_block = True
    position = 0
    for d in data:
        d = int(d)
        if is_block:
            blocks.append((position, d))
        position += d

        is_block = not is_block

    return blocks


def block_string(blocks):
    string = ''
    position = 0
    for bi, (p, l) in enumerate(blocks):
        while position < p:
            string += EMPTY
            position += 1
        string += f'{bi}'*l
        position += l

    return string

def make_memory(blocks):
    memory = []
    position = 0
    for bi, (p, l) in enumerate(blocks):
        while position < p:
            memory.append(None)
            position += 1
        memory += [bi]*l
        position += l

    return memory

def compacted_memory_checksum(memory : list):
    j = len(memory) - 1
    checksum = 0
    for i in range(len(memory)):
        
        if memory[i] is None:
            # Use j value, then decrease it
            id = memory[j]
            j -= 1
            while (memory[j] is None):
                # Keep decreasing it
                j -= 1
        else:
            # Use i value
            id = memory[i]
        checksum += i * id

        if j <= i:
            break

    return checksum


def main():
    file = sys.argv[1]
    
    with open(file) as f:
        data = f.read()

        blocks = parse(data)

        memory = make_memory(blocks)

        print(compacted_memory_checksum(memory))

        

if __name__ == '__main__':
    main()