from pyjvm.execution.execution import bytecode, Executor
from pyjvm.types import NULL_VALUE, Integer, Long, Float, Double


@bytecode('nop')
class NoOp(Executor):
    def execute(self):
        pass


def _create_constant_dict():
    d = {
        'aconst_null': NULL_VALUE,
        'iconst_m1': Integer.create_instance(-1)
    }

    for int_value in range(6):
        d['iconst_' + str(int_value)] = Integer.create_instance(int_value)

    for long_value in range(2):
        d['lconst_' + str(long_value)] = Long.create_instance(long_value)

    for float_value in range(2):
        d['lfloat_' + str(float_value)] = Float.create_instance(float_value)

    for double_value in range(2):
        d['dconst_' + str(double_value)] = Double.create_instance(double_value)

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
