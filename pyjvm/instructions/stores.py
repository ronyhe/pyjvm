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


def _store_into_array_decorator(class_):
    type_letters = 'lfdibcsa'
    for letter in type_letters:
        class_ = bytecode(letter + 'astore')(class_)

    return class_


@_store_into_array_decorator
class StoreIntoArray(Instructor):
    def execute(self):
        value, index, array = (self.peek_op_stack(i) for i in range(3))
        return IncrementProgramCounter.after(
            actions.StoreIntoArray(array=array, index=index.value, value=value),
            Pop(3)
        )
