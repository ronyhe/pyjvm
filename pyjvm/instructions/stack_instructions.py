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
