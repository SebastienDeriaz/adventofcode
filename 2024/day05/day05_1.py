import re
import sys

ORDER_PATTERN = '(\d+)\|(\d+)'
UPDATE_PATTERN = '\d+(?:,\d+)+'



def parse_orders_updates(data):
    orders = {}
    updates = []
    for a, b in re.findall(ORDER_PATTERN, data):
        a = int(a)
        b = int(b)
        if a in orders:
            orders[a].append(b)
        else:
            orders[a] = [b]
    
    for update in re.findall(UPDATE_PATTERN, data):
        updates.append([int(x) for x in update.split(',')])

    return orders, updates


def main():
    file = sys.argv[1]

    with open(file) as f:
        data = f.read()

        orders, updates = parse_orders_updates(data)


        middle_numbers = []
        for update in updates:
            keep = True
            for i, x in enumerate(update):
                if x in orders:
                    for y in orders[x]:
                        if y in update and update.index(y) < i:
                            # Reject it
                            keep = False
                            break
                if not keep:
                    break
            else:
                if len(update) % 2 != 1:
                    raise ValueError('Cannot find middle number of even-lengthed update')
                # This update is valid
                middle_numbers.append(update[(len(update)-1)//2])
        print(sum(middle_numbers))

if __name__ == '__main__':
    main()


