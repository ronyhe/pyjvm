import operator

from pyjvm.instructions.instructions import Executor, bytecode
from pyjvm.instructions.verifiers import verifier_by_type
from pyjvm.jvm_types import min_max_by_type, Integer, Long, Double, Float


def _letter(type_):
    if type_ == Integer:
        return 'i'
    elif type_ == Double:
        return 'd'
    elif type_ == Float:
        return 'f'
    elif type_ == Long:
        return 'l'
    else:
        raise ValueError()


class BinarySpec:
    def __init__(self, name, op, types=None):
        if types is None:
            self.types = Integer, Float, Double, Long
        else:
            self.types = types
        self.name = name
        self.op = op

    def create_specs(self):
        return [self.create_single_spec(type_) for type_ in self.types]

    def create_single_spec(self, type_):
        name = _letter(type_) + self.name
        return name, type_, self.op


class IntegralBinarySpec(BinarySpec):
    def __init__(self, name, op):
        super().__init__(name, op, (Integer, Long))


_SPECS = (
    BinarySpec('add', operator.add),
    BinarySpec('sub', operator.sub),
    BinarySpec('mul', operator.mul),
    BinarySpec('div', operator.truediv),
    BinarySpec('rem', operator.mod),
    BinarySpec('neg', operator.neg),

    IntegralBinarySpec('shl', operator.lshift),
    IntegralBinarySpec('shr', operator.rshift),
    IntegralBinarySpec('and', operator.and_),
    IntegralBinarySpec('or', operator.or_),
    IntegralBinarySpec('xor', operator.xor)
)


def _binary_decorator(the_class):
    for descriptor in _SPECS:
        for name, type_, op in descriptor.create_specs():
            the_class = bytecode(name, type_, op)(the_class)

    return the_class


@_binary_decorator
class BinOp(Executor):
    def __init__(self, instruction, machine, type_, operator_):
        super().__init__(instruction, machine)
        self.type = type_
        self.operator = operator_

    def execute(self):
        stack = self.machine.current_op_stack()
        operands = [stack.pop(), stack.pop()]
        verifier = verifier_by_type(self.type)
        for op in operands:
            verifier(op)
        values = [op.value for op in operands]
        raw_result = self.operator(*values)
        min_, max_ = min_max_by_type(self.type)
        if raw_result < min_ or raw_result > max_:
            raise OverflowError('Non-JVM-compliant error. Result of math instruction out of range')
        result = self.type.create_instance(raw_result)
        stack.push(result)
