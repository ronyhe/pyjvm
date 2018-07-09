from pyjvm import actions
from pyjvm.actions import IncrementProgramCounter
from pyjvm.instructions.instructions import Instructor, bytecode


@bytecode('pop', 1)
@bytecode('pop2', 2)
class Pop(Instructor):
    def __init__(self, inputs, amount):
        super().__init__(inputs)
        self.amount = amount

    def execute(self):
        return IncrementProgramCounter.after(
            actions.Pop(self.amount)
        )


@bytecode('dup')
class Duplicate(Instructor):
    def execute(self):
        return IncrementProgramCounter.after(
            actions.Push(self.peek_op_stack())
        )


@bytecode('dup_x1')
class DuplicateX1(Instructor):
    def execute(self):
        top = self.peek_op_stack()
        ante_top = self.peek_op_stack(1)
        return IncrementProgramCounter.after(
            actions.Pop(2),
            actions.Push(top),
            actions.Push(ante_top),
            actions.Push(top)
        )
