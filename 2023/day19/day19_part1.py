from sys import argv
import re
from enum import Enum


class Category(Enum):
    EXTREMELY_COOL_LOOKING = 0
    MUSICAL = 1
    AERODYNAMIC = 2
    SHINY = 3

ACCEPT_WORKFLOW = 'A'
REFUSE_WORKFLOW = 'R'
START_WORKFLOW = 'in'


def parse_condition(description):
    SMALLER_THAN = '<'
    GREATER_THAN = '>'
    compare_pattern = '(\w+)([<>])(\d+):(\w+)'
    m = re.match(compare_pattern, description)
    if m:
        operation = lambda a,b : a < b if m.group(2) == SMALLER_THAN else a > b
        # It is a compare condition
        return lambda parts_categories : (operation(parts_categories[m.group(1)], int(m.group(3))), m.group(4))

    else:
        # It is an affirmation
        return lambda _ : (True, description)

class Part:
    def __init__(self, string_description : str) -> None:
        pattern = '\{([\w=\d,]+)\}'
        category_pattern = '(\w)=(\d+)'
        m = re.match(pattern, string_description)
        self._categories = {}
        for category in m.group(1).split(','):
            m = re.match(category_pattern, category)
            _type = m.group(1)
            value = int(m.group(2))
            self._categories[_type] = value 
            
    def categories(self):
        return self._categories

    def __repr__(self) -> str:
        return ','.join([f'{t}={v}' for t, v in self._categories.items()])

class Workflow:
    def __init__(self, string_description : str) -> None:
        pattern = '(\w+)\{([\w<>\d:,]+)\}'
        m = re.match(pattern, string_description)
        self.id = m.group(1)
        self.conditions = []
        for condition in m.group(2).split(','):
            self.conditions.append(parse_condition(condition))
    
    def check_part(self, part : Part):
        for condition in self.conditions:
            accepted, next_workflow_id = condition(part.categories())
            if accepted:
                return next_workflow_id
        raise RuntimeError(f'Couldn\'t find a category for the part : {part}')


def parse_file(data : str):
    workflows_str, parts_str = data.split('\n\n')
    workflows = {}
    for line in workflows_str.split('\n'):
        if line != '':
            wf = Workflow(line)
            workflows[wf.id] = wf

    parts = []
    for line in parts_str.split('\n'):
        if line != '':
            parts.append(Part(line))

    return workflows, parts


def main():
    file = argv[1]
    with open(file) as f:
        data = f.read()
        workflows, parts = parse_file(data)

        N = 0

        for part in parts:
            w = workflows[START_WORKFLOW]
            w : Workflow
            while True:
                print(f'Part {part}')
                new_w = w.check_part(part)
                if new_w == ACCEPT_WORKFLOW:
                    print(f'  accept')
                    N += sum(part.categories().values())
                    break
                elif new_w == REFUSE_WORKFLOW:
                    print(f'  refuse')
                    break
                w = workflows[new_w]

        print(N)
        

if __name__ == '__main__':
    main()