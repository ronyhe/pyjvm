from pyjvm.execution.execution import bytecode, Executor
from pyjvm.types import NULL_VALUE, Integer


@bytecode('nop')
class NoOp(Executor):
    def execute(self):
        pass


def _create_constant_dict():
    d = {
        'aconst_null': NULL_VALUE,
        'iconst_m1': Integer.create_instance(-1)
    }

    for i in range(6):
        d['iconst_' + str(i)] = Integer.create_instance(i)

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
