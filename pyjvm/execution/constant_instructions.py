from pyjvm.execution.execution import bytecode, Executor
from pyjvm.types import NULL_VALUE


@bytecode('nop')
class NoOp(Executor):
    def execute(self):
        pass


# noinspection SpellCheckingInspection
@bytecode('aconst_null', NULL_VALUE)
class Push(Executor):
    def __init__(self, instruction, machine, value):
        super().__init__(instruction, machine)
        self.value = value

    def execute(self):
        self.machine.current_op_stack().push(self.value)
