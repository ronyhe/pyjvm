from pyjvm.instructions.instructions import bytecode, Executor
from pyjvm.jvm_types import NULL_VALUE, Integer, Long, Float, Double


@bytecode('nop')
@bytecode('monitorenter')
@bytecode('monitorexit')
class NoOp(Executor):
    def execute(self):
        pass


def _create_constant_dict():
    d = {
        'aconst_null': NULL_VALUE,
        'iconst_m1': Integer.create_instance(-1)
    }

    specs = (
        (Integer, 'i', 5),
        (Long, 'l', 1),
        (Float, 'f', 2),
        (Double, 'd', 1),
    )

    for type_, prefix, max_index in specs:
        for i in range(max_index + 1):
            mnemonic = f'{prefix}const_{i}'
            value = type_.create_instance(i)
            d[mnemonic] = value

    return d


def constants_decorator(the_class):
    for name, value in _create_constant_dict().items():
        func = bytecode(name, value)
        the_class = func(the_class)

    return the_class


@constants_decorator
class Push(Executor):
    def __init__(self, instruction, machine, value):
        super().__init__(instruction, machine)
        self.value = value

    def execute(self):
        self.machine.current_op_stack().push(self.value)


@bytecode('bipush')
@bytecode('sipush')
class PushIntegerOperand(Executor):
    def execute(self):
        operand = self.instruction.operands[0].value
        value = Integer.create_instance(int(operand))
        self.machine.current_op_stack().push(value)
