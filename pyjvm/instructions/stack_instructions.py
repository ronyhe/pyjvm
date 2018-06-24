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
