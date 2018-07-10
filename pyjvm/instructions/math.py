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


class BinaryOperator:
    def __init__(self, name, op, types):
        self.name = name
        self.op = op
        self.types = types

    @classmethod
    def all_types(cls, name, op):
        return cls(name, op, _ALL_TYPES)

    @classmethod
    def integral_types(cls, name, op):
        return cls(name, op, _INTEGRAL_TYPES)

    def bytecode_args(self):
        dic = {}
        for type_ in self.types:
            letter = TYPE_LETTERS[type_]
            name = letter + self.name
            dic[name] = [self.op, type_]

        return dic


OPERATORS = (
    BinaryOperator.all_types('add', operator.add),
    BinaryOperator.all_types('sub', operator.sub),
    BinaryOperator.all_types('mul', operator.mul),
    BinaryOperator.all_types('div', operator.truediv),
    BinaryOperator.all_types('rem', operator.mod),

    BinaryOperator.integral_types('shl', operator.lshift),
    BinaryOperator.integral_types('shr', operator.rshift),
    BinaryOperator.integral_types('and', operator.and_),
    BinaryOperator.integral_types('or', operator.or_),
    BinaryOperator.integral_types('xor', operator.xor)
)


def _create_bytecode_dict():
    dic = {}
    for op in OPERATORS:
        dic.update(op.bytecode_args())

    return dic


@bytecode_dict(_create_bytecode_dict())
class BinaryMath(Instructor):
    def __init__(self, inputs, op, type_):
        super().__init__(inputs)
        self.op = op
        self.type = type_

    def execute(self):
        right = self.peek_op_stack(0)
        left = self.peek_op_stack(1)
        value = self.op(left.value, right.value)
        result = self.type.create_instance(value)
        return IncrementProgramCounter.after(
            actions.Pop(2),
            actions.Push(result)
        )

# add neg and iinc
