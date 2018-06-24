from pyjvm.instructions.instructions import Executor, bytecode


@bytecode('pop', 1)
@bytecode('pop2', 2)
class Pop(Executor):
    def __init__(self, instruction, machine, amount):
        super().__init__(instruction, machine)
        self.amount = amount

    def execute(self):
        for _ in range(self.amount):
            self.machine.current_op_stack().pop()


@bytecode('dup', 0)
@bytecode('dup_x1', 2)
class Duplicate(Executor):
    def __init__(self, instruction, machine, insertion_off_set_from_top):
        super().__init__(instruction, machine)
        self.insertion_off_set_from_top = insertion_off_set_from_top

    def execute(self):
        value = self.machine.current_op_stack().peek().duplicate()
        self.machine.current_op_stack().insert_at_offset(self.insertion_off_set_from_top, value)
