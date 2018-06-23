from pyjvm.execution.execution import bytecode, Executor
from pyjvm.types import NULL_VALUE, Integer


@bytecode('nop')
class NoOp(Executor):
    def execute(self):
        pass


@bytecode('aconst_null', NULL_VALUE)
@bytecode('iconst_0', Integer.create_instance(0))
@bytecode('iconst_1', Integer.create_instance(1))
@bytecode('iconst_2', Integer.create_instance(2))
@bytecode('iconst_3', Integer.create_instance(3))
@bytecode('iconst_4', Integer.create_instance(4))
@bytecode('iconst_5', Integer.create_instance(5))
class Push(Executor):
    def __init__(self, instruction, machine, value):
        super().__init__(instruction, machine)
        self.value = value

    def execute(self):
        self.machine.current_op_stack().push(self.value)
