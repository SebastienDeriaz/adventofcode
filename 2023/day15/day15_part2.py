from sys import argv
from functools import reduce

class Step:
    ADD_SYMBOL = '='
    REMOVE_SYMBOL = '-'
    def __init__(self, description : str) -> None:
        self._add_nRemove = self.ADD_SYMBOL in description
        separator = self.ADD_SYMBOL if self._add_nRemove else self.REMOVE_SYMBOL
        id, focal_length = description.split(separator)
        self._id = id
        if focal_length is not None and focal_length != '':
            self._focal = int(focal_length)
    
    def __repr__(self) -> str:
        if self._add_nRemove:
            return f'+{self._id}/{self.box_number()}({self._focal})'
        else:
            return f'-{self._id}/{self.box_number()}'

    def is_add(self):
        return self._add_nRemove

    def box_number(self):
        return hash_step(self._id)

    def lens_id(self):
        return self._id

    def focal(self):
        return self._focal

def parse_sequence(data):
    return [Step(step) for step in data.replace('\n', '').split(',') if step != '']

def hash_step(step):
    def f(n, b):
        return ((n + ord(b)) * 17) % 256
    return reduce(f, step, 0)

def parse_step(step):
    if '-' in step:
        return ()

def initialize_boxes(steps : list):
    N_boxes = 256
    empty_box = []
    boxes = [empty_box.copy() for _ in range(N_boxes)]

    step : Step
    for step in steps:
        lens_index = next((i for i, x in enumerate(boxes[step.box_number()]) if x[0] == step.lens_id()), None)
        if step.is_add():
            # Check if the lens aready exists
            if lens_index is not None:
                # Replace it
                boxes[step.box_number()][lens_index] = (step.lens_id(), step.focal())
            else:
                # Add it
                boxes[step.box_number()].append((step.lens_id(), step.focal()))
        elif lens_index is not None:
            # Remove it
            boxes[step.box_number()].remove(boxes[step.box_number()][lens_index])

    return boxes

def focusing_power(boxes):
    power = 0
    for i, b in enumerate(boxes):
        for il, (_, focal) in enumerate(b):
            power += (i+1) * focal * (il+1)
    return power

def main():
    file = argv[1]
    with open(file) as f:
        data = f.read()
        steps = parse_sequence(data)
        boxes = initialize_boxes(steps)
        print(focusing_power(boxes))


if __name__ == '__main__':
    main()