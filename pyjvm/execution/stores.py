from pyjvm.execution.execution import Executor


class StoreToLocalVariable(Executor):
    def __init__(self, instruction, machine, index_into_locals=None, ensure_type=None):
        super().__init__(instruction, machine)
        self.ensure_type = ensure_type
        if index_into_locals is None:
            self.index_into_locals = int(self.instruction.operands[0].value)
        else:
            self.index_into_locals = index_into_locals

    def execute(self):
        value = self.machine.current_op_stack().pop()
        if self.ensure_type is not None and not self.ensure_type == value.type:
            self.raise_type_error(value.type)
        self.machine.current_locals().store(self.index_into_locals, value)

    def raise_type_error(self, type_):
        message = f'Instruction {self.instruction.name} expects ' \
                  f'top-of-stack to have value of type {self.ensure_type}, but TOS has {type_}'
        raise TypeError(message)
