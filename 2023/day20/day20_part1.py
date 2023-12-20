# Do everything in order, treat all the pulses from a module before doing the next one
# Every module can bit a position in a bitfield
# Every module output can be represented by a mask and a value
#
# Broadcaster/unnamed : multiply its value bit by its output mask
# Flip-Flop : Multiply its output mask by inverted input bit (to ignore high pulse)
#   Update its current state to be xor the old one
#   Send a pulse accoding to its value
# Conjonction : Special type, it occupies N bits (N inputs), output is `and` of all bits, inverted, times the mask
#
# Maybe using bit fields is not the right approach, it is necessary to treat each module separately, so merging them into a bitfield makes little sense


from sys import argv
import re
from enum import Enum

class Pulse:
    def __init__(self, source, destination ,value) -> None:
        self.source = source
        self.destination = destination
        self.value = value
    
    def __repr__(self) -> str:
        return f'{self.source} -{"high" if self.value else "low"}-> {self.destination}'

class Module:
    def __init__(self, id : str, outputs : list) -> None:
        self._outputs = outputs
        self._id = id

    def simulate(self, pulse, _) -> list:
        return [Pulse(self._id, m, pulse) for m in self._outputs]

    def __repr__(self) -> str:
        return f'{self._id}->{",".join(self._outputs)}'

    def reset(self):
        pass

    def id(self):
        return self._id

    def outputs(self):
        return self._outputs

class FlipFlopModule(Module):
    def __init__(self, id : str, outputs : list) -> None:
        super().__init__(id, outputs)
        self.reset()
    
    def reset(self):
        self._state = 0

    def simulate(self, pulse, _) -> list:
        if pulse == 0:
            self._state = 1 - self._state
            return [Pulse(self._id, m, self._state) for m in self._outputs]
        else:
            return []

    def __repr__(self) -> str:
        return f'%{self._id}->{",".join(self._outputs)}'

class ConjonctionModule(Module):
    def __init__(self, id : str, outputs : list) -> None:
        super().__init__(id, outputs)
        self._inputs = {}

    def reset(self):
        self._inputs = {k : 0 for k in self._inputs}

    def simulate(self, pulse, input) -> list:
        self._inputs[input] = pulse
        value = 1 - int(all(self._inputs.values()))
        return [Pulse(self._id, m, value) for m in self._outputs]

    def add_input(self, input : str):
        self._inputs[input] = 0

    def __repr__(self) -> str:
        return f'&{self._id}->{",".join(self._outputs)}'

class Simulator:
    FLIP_FLOP_SYMBOL = '%'
    CONJONCTION_SYMBOL = '&'

    class Type(Enum):
        STANDARD = 0
        FLIP_FLOP = 1
        CONJONCTION = 2


    def __init__(self) -> None:
        self._modules = {}

    def load_schematic(self, schematic : str):
        pattern = '([%&\w]+) -> ([\w, ]+)'
        for line in schematic.split('\n'):
            if line != '':
                m = re.match(pattern, line)
                module_id_raw = m.group(1)
                if self.FLIP_FLOP_SYMBOL in module_id_raw or self.CONJONCTION_SYMBOL in module_id_raw:
                    module_id = module_id_raw[1:]
                else:
                    module_id = module_id_raw
                
                outputs = m.group(2).replace(' ', '').split(',')
                for o in outputs:
                    if o in self._modules and isinstance(self._modules[o], ConjonctionModule):
                        self._modules[o].add_input(module_id)
                if self.FLIP_FLOP_SYMBOL in module_id_raw:
                    self._modules[module_id] = FlipFlopModule(module_id, outputs)
                elif self.CONJONCTION_SYMBOL in module_id_raw:
                    self._modules[module_id] = ConjonctionModule(module_id, outputs)
                    for _, m in self._modules.items():
                        for o in m.outputs():
                            if o in self._modules and isinstance(self._modules[o], ConjonctionModule):
                                self._modules[o].add_input(m.id())
                else:
                    self._modules[module_id] = Module(module_id, outputs)

    def simulate(self, pulse_value=0, entry_point='broadcaster'):
        high = 0
        low = 0
        queue = [Pulse('button', entry_point, pulse_value)]
        while len(queue) > 0:
            new_queue = []
            
            pulse : Pulse
            for pulse in queue:
                if pulse.value == 0:
                    low += 1
                else:
                    high += 1

                if pulse.destination in self._modules:
                    new_queue += self._modules[pulse.destination].simulate(pulse.value, pulse.source)
                else:
                    # Ignore it
                    pass

            queue = new_queue

        return low, high


def main():
    file = argv[1]
    simulator = Simulator()
    with open(file) as f:
        simulator.load_schematic(f.read())
        N = [0, 0]
        for i in range(1000):
            N = [(n + x) for n, x in zip(N, simulator.simulate())]

        print(N[0] * N[1])



if __name__ == '__main__':
    main()