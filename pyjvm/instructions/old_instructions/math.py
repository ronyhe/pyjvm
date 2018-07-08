import operator

from pyjvm.instructions.instructions import Executor, bytecode
from pyjvm.instructions.old_instructions.verifiers import verifier_by_type
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


def _validate_range(type_, raw_value):
    min_, max_ = min_max_by_type(type_)
    if raw_value < min_ or raw_value > max_:
        raise OverflowError('Non-JVM-compliant error. Result of math instruction out of range')


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
        _validate_range(self.type, raw_result)
        result = self.type.create_instance(raw_result)
        stack.push(result)


@bytecode('iinc')
class IncrementLocal(Executor):
    def execute(self):
        ops = self.instruction.operands
        index_in_locals, value_to_add = (int(op.value) for op in ops)

        locals_ = self.machine.current_locals()
        local = locals_.load(index_in_locals)

        new_value = local.value + value_to_add
        _validate_range(Integer, new_value)
        new_local = Integer.create_instance(new_value)

        locals_.store(index_in_locals, new_local)
