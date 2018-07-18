import itertools
from collections import OrderedDict

from jawa.util.bytecode import Instruction

from pyjvm.utils import literal_operand, pull_pairs

LOOKUP_SWITCH = 'lookupswitch'
TABLE_SWITCH = 'tableswitch'


def _int_value(v):
    try:
        return v.value
    except AttributeError:
        return int(v)


def _create_operands(values):
    return [literal_operand(v) for v in values]


def _create_instruction(name, pos, operands):
    ops = _create_operands(operands)
    instruction = Instruction.create(name, ops)
    if pos is not None:
        # noinspection PyProtectedMember
        instruction = instruction._replace(pos=pos)
    return instruction


def _ints_from_instruction(instruction):
    return [int(o.value) for o in instruction.operands]


def _validate_instruction_name(instruction, name):
    if not instruction.mnemonic == name:
        raise ValueError(f'A {name} object can only be created from a {name} instruction')


class LookupSwitch:
    def __init__(self, default, value_offset_pairs):
        self.default = default
        self.pairs = OrderedDict(value_offset_pairs)

    def create_instruction(self, position=None):
        flat_pairs = itertools.chain(*self.pairs.items())
        return _create_instruction(LOOKUP_SWITCH, position, [
            self.default,
            len(self.pairs),
            *flat_pairs
        ])

    def find_offset(self, value):
        value = _int_value(value)

        try:
            return self.pairs[value]
        except KeyError:
            return self.default

    @classmethod
    def from_instruction(cls, instruction):
        _validate_instruction_name(instruction, LOOKUP_SWITCH)
        default, num_pairs, *flat = _ints_from_instruction(instruction)
        pairs = pull_pairs(flat)
        return cls(default, pairs)


class TableSwitch:
    def __init__(self, default, offsets):
        self.default = default
        self.offsets = sorted(offsets)
        self.low = self.offsets[0]
        self.high = self.offsets[len(self.offsets) - 1]

    def find_offset(self, value):
        offsets = self.offsets
        value = _int_value(value)

        if value < self.low or value > self.high:
            offset = self.default
        else:
            index = value - self.low
            offset = offsets[index]

        return offset

    def create_instruction(self, position=None):
        return _create_instruction(TABLE_SWITCH, position, [
            self.default,
            self.low,
            self.high,
            *self.offsets
        ])

    @classmethod
    def from_instruction(cls, instruction):
        _validate_instruction_name(instruction, TABLE_SWITCH)
        default, low, high, *offsets = _ints_from_instruction(instruction)
        return cls(default, offsets)
