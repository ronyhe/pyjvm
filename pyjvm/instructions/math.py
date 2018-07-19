import functools
import operator

from pyjvm import actions
from pyjvm.actions import IncrementProgramCounter
from pyjvm.instructions.instructions import bytecode_dict, Instructor
from pyjvm.jvm_types import Integer, Long, Float, Double

TYPE_LETTERS = {
    Integer: 'i',
    Long: 'l',
    Double: 'd',
    Float: 'f'
}
_ALL_TYPES = list(TYPE_LETTERS.keys())
_INTEGRAL_TYPES = [Integer, Long]


def _logical_right_shift(a, b):
    return (a % 0x100000000) >> b


class MathOperation:
    def __init__(self, name, op, types, operands):
        self.name = name
        self.op = op
        self.types = types
        self.operands = operands

    @classmethod
    def all_types(cls, name, op, operands=2):
        return cls(name, op, _ALL_TYPES, operands)

    @classmethod
    def integral_types(cls, name, op, operands=2):
        return cls(name, op, _INTEGRAL_TYPES, operands)

    def bytecode_args(self):
        dic = {}
        for type_ in self.types:
            letter = TYPE_LETTERS[type_]
            name = letter + self.name
            dic[name] = [self.op, type_, self.operands]

        return dic


OPERATORS = (
    MathOperation.all_types('add', operator.add),
    MathOperation.all_types('sub', operator.sub),
    MathOperation.all_types('mul', operator.mul),
    MathOperation.all_types('div', operator.truediv),
    MathOperation.all_types('rem', operator.mod),

    MathOperation.all_types('neg', operator.neg, operands=1),
    MathOperation('inc', functools.partial(operator.add, 1), [Integer], operands=1),

    MathOperation.integral_types('shl', operator.lshift),
    MathOperation.integral_types('shr', operator.rshift),
    MathOperation.integral_types('and', operator.and_),
    MathOperation.integral_types('or', operator.or_),
    MathOperation.integral_types('xor', operator.xor),

    MathOperation.integral_types('ushr', _logical_right_shift)
)


def _create_bytecode_dict():
    dic = {}
    for op in OPERATORS:
        dic.update(op.bytecode_args())

    return dic


@bytecode_dict(_create_bytecode_dict())
class BinaryMath(Instructor):
    def __init__(self, inputs, op, type_, ops):
        super().__init__(inputs)
        self.op = op
        self.type = type_
        self.ops = ops

    def execute(self):
        ops = reversed(list(self.peek_many(self.ops)))
        value = self.op(*(op.value for op in ops))
        result = self.type.create_instance(value)
        return IncrementProgramCounter.after(
            actions.Pop(self.ops),
            actions.Push(result)
        )
