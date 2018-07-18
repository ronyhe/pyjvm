import itertools
from collections import OrderedDict

from jawa.util.bytecode import Instruction

from pyjvm import actions
from pyjvm.instructions.instructions import Instructor, bytecode_list, bytecode
# noinspection SpellCheckingInspection
from pyjvm.utils import pull_pairs
from test.utils import literal_operand

LOOKUPSWITCH = 'lookupswitch'

_RETURN_LETTERS = 'ilfda'
RETURN_RESULT_INSTRUCTIONS = [
    letter + 'return' for letter in _RETURN_LETTERS
]


@bytecode_list(RETURN_RESULT_INSTRUCTIONS)
class ReturnResult(Instructor):
    def execute(self):
        result = self.peek_op_stack()
        return actions.ReturnResult(result)


@bytecode('return')
class ReturnVoid(Instructor):
    def execute(self):
        return actions.ReturnVoid()


@bytecode_list([
    'goto',
    'goto_w'
])
class GoTo(Instructor):
    def execute(self):
        source = self.instruction.pos
        offset = self.operand_as_int()
        target = source + offset
        return actions.GoTo(target)


class LookupSwitch:
    def __init__(self, default, value_offset_pairs):
        self.default = default
        self.pairs = OrderedDict(value_offset_pairs)

    def create_instruction(self, position=None):
        flat_pairs = itertools.chain(*self.pairs.items())
        instruction = Instruction.create('lookupswitch', [
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
