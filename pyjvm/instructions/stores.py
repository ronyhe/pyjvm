from pyjvm import actions
from pyjvm.actions import IncrementProgramCounter, Pop
from pyjvm.instructions.instructions import bytecode, Instructor


def _store_into_locals_decorator(class_):
    # noinspection SpellCheckingInspection
    type_letters = 'ilfda'
    indexes_in_locals = [None, 0, 1, 2, 3]
    for letter in type_letters:
        for index in indexes_in_locals:
            suffix = '_' + str(index) if index is not None else ''
            mnemonic = letter + 'store' + suffix
            class_ = bytecode(mnemonic, index)(class_)

    return class_


@_store_into_locals_decorator
class StoreIntoLocals(Instructor):
    def __init__(self, inputs, index_in_locals=None):
        super().__init__(inputs)
        if index_in_locals is None:
            self.index_in_locals = self.operand_as_int()
        else:
            self.index_in_locals = index_in_locals

    def execute(self):
        return IncrementProgramCounter.after(
            actions.StoreInLocals(index=self.index_in_locals, value=self.peek_op_stack()),
            Pop()
        )
