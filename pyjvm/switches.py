import itertools
from collections.__init__ import OrderedDict

from jawa.util.bytecode import Instruction

from pyjvm.utils import literal_operand, pull_pairs


class LookupSwitch:
    def __init__(self, default, value_offset_pairs):
        self.default = default
        self.pairs = OrderedDict(value_offset_pairs)

    def create_instruction(self, position=None):
        flat_pairs = itertools.chain(*self.pairs.items())
        instruction = Instruction.create(LOOKUPSWITCH, [
            literal_operand(self.default),
            literal_operand(len(self.pairs)),
            *(literal_operand(n) for n in flat_pairs)
        ])

        if position is not None:
            # noinspection PyProtectedMember
            instruction = instruction._replace(pos=position)

        return instruction

    def find_offset(self, value):
        try:
            value = value.value
        except AttributeError:
            value = int(value)

        try:
            return self.pairs[value]
        except KeyError:
            return self.default

    @classmethod
    def from_instruction(cls, instruction):
        name = LOOKUPSWITCH
        if not instruction.mnemonic == name:
            raise ValueError(f'A {name} object can only be created from a {name} instruction')
        ops = [int(op.value) for op in instruction.operands]
        default, num_pairs, *flat = ops
        pairs = pull_pairs(flat)
        return cls(default, pairs)


LOOKUPSWITCH = 'lookupswitch'
