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

def get_bad_updates(updates, orders):
    output = []
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
                output.append(update)
                break
    return output


def repair_updates(bad_updates, orders):
    bad_update: list
    good_updates = []

    for bad_update in bad_updates:
        while True:
            stop = False
            for i in range(len(bad_update)):
                x = bad_update[i]
                if x in orders:
                    for y in orders[x]:
                        if y in bad_update:
                            # Check if any y is below x, if that is the case, put x before y
                            y_pos = bad_update.index(y)
                            if y_pos < i:
                                bad_update.remove(x)
                                bad_update.insert(y_pos, x)
                                # Restart
                                stop = True
                                break
                if stop:
                    break
            else:
                # OK !
                good_updates.append(bad_update)
                break

    return good_updates


def main():
    file = sys.argv[1]

    with open(file) as f:
        data = f.read()

        orders, updates = parse_orders_updates(data)

        bad_updates = get_bad_updates(updates, orders)
        
        repaired_updates = repair_updates(bad_updates, orders)

        print(sum([l[(len(l)-1)//2] for l in repaired_updates]))
    

if __name__ == '__main__':
    main()


