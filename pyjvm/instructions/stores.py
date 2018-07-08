from pyjvm import actions
from pyjvm.actions import IncrementProgramCounter, Pop
from pyjvm.instructions.instructions import bytecode, Instructor


@bytecode('istore')
class StoreIntegerInLocals(Instructor):
    def execute(self):
        index = int(self.instruction.operands[0].value)
        return IncrementProgramCounter.after(
            actions.StoreInLocals(index=index, value=self.op_stack.peek()),
            Pop()
        )
