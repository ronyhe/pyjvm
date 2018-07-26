import operator

from pyjvm import actions
from pyjvm.actions import IncrementProgramCounter
from pyjvm.instructions.instructions import bytecode_dict, Instructor, bytecode
from pyjvm.model.jvm_types import Integer, Long, Float, Double

TYPE_LETTERS = {
    Integer: 'i',
    Long: 'l',
    Double: 'd',
    Float: 'f'
}
_ALL_TYPES = list(TYPE_LETTERS.keys())
_INTEGRAL_TYPES = [Integer, Long]


def _logical_right_shift(a, b):
    # Taken from: https://stackoverflow.com/a/5833119/3129333
    return (a % 0x100000000) >> b


class MathOperation:
    """A description of a math instruction

    This includes:
     - `name`
     - `op` A function that takes `operands` amount of arguments and returns the result of the computation
     - `types` The types for which this instruction should exists
     - `operands` The amount of operands to send to `op`
    """

    def __init__(self, name, op, types, operands):
        self.name = name
        self.op = op
        self.types = types
        self.operands = operands

    @classmethod
    def all_types(cls, name, op, operands=2):
        """Returns a `MathOperation` instance that should apply to all numeric types"""
        return cls(name, op, _ALL_TYPES, operands)

    @classmethod
    def integral_types(cls, name, op, operands=2):
        """Returns a `MathOperation` instance that should apply to all integral types"""
        return cls(name, op, _INTEGRAL_TYPES, operands)

    def bytecode_args(self):
        """Returns a dictionary from instruction names to a list of arguments

        The instruction names are created according to `self.types`
        The list of arguments has the arguments that the `MathInstructor` expects.

        For example an operation that was created like this:
            .. code::

                MathOperation('name', some_func, [Integer, Float], 2)

        Will produce this when `bytecode_args` is called:
            .. code::

                {
                    'iname': [some_func, Integer, 2],
                    'fname': [some_func, Float, 2],
                }
        """
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

    MathOperation.integral_types('shl', operator.lshift),
    MathOperation.integral_types('shr', operator.rshift),
    MathOperation.integral_types('and', operator.and_),
    MathOperation.integral_types('or', operator.or_),
    MathOperation.integral_types('xor', operator.xor),

    MathOperation.integral_types('ushr', _logical_right_shift)
)


def _create_bytecode_dict():
    """Collect all `OPERATORS` into a single bytecode_dict"""
    dic = {}
    for op in OPERATORS:
        dic.update(op.bytecode_args())

    return dic


@bytecode_dict(_create_bytecode_dict())
class MathInstructor(Instructor):
    """Pops values and pushed the result of a math operation

    The general process goes like this:
     - Pop `ops` amount of values
     - Send them to `op`
     - Wrap the result as an instance of `type_`
     - Push the wrapped result
    """

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


@bytecode('iinc')
class Increment(Instructor):
    """Implements the iinc instruction

    The instruction loads a value from locals at an index that's provided as an operand
    It adds another value to it, also provided as an operand.
    And then it pushes the result
    """

    def execute(self):
        local_index, amount_to_add = [op.value for op in self.instruction.operands]
        original_value = self.locals.load(local_index).value
        new_value = original_value + amount_to_add
        new_instance = Integer.create_instance(new_value)
        return IncrementProgramCounter.after(
            actions.Push(new_instance)
        )
