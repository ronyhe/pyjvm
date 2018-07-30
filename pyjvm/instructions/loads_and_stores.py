from pyjvm.core import actions
from pyjvm.core.actions import IncrementProgramCounter, Pop
from pyjvm.instructions.instructions import Instructor, bytecode_dict, bytecode_list


def _create_store_load_dict(phrase):
    """Create an instruction dictionary of the load or store instructions

    For example, with the phrase 'load'
    {
        'iload': [None],
        'iload_0': [0],
        ...
        'aload_3: [3]
    }
    """

    # noinspection SpellCheckingInspection
    type_letters = 'ilfda'
    indexes_in_locals = [None, 0, 1, 2, 3]
    dic = {}

    def create_args(i):
        if i is None:
            return [None]
        else:
            return [i]

    for letter in type_letters:
        for index in indexes_in_locals:
            suffix = '_' + str(index) if index is not None else ''
            mnemonic = letter + phrase + suffix
            dic[mnemonic] = create_args(index)

    return dic


def _create_into_array_list(phrase):
    """Create load or store into array instructions

    For example, with the phrase 'astore':
    [
        'iastore',
        'fastore',
        ...
        'aastore'
    ]
    """

    # noinspection SpellCheckingInspection
    return [letter + phrase for letter in 'lfdibcsa']


_STORE = bytecode_dict(_create_store_load_dict('store'))
_LOAD = bytecode_dict(_create_store_load_dict('load'))
_STORE_INTO_ARRAY = bytecode_list(_create_into_array_list('astore'))
_LOAD_FROM_ARRAY = bytecode_list(_create_into_array_list('aload'))


@_STORE
class StoreIntoLocals(Instructor):
    """Pops stack and stores the value in to locals at `index_in_locals`

    If `index_in_locals` is None, the index is taken from the instruction operand.
    """

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


@_STORE_INTO_ARRAY
class StoreIntoArray(Instructor):
    """Pops `value`, `index` and `array` from stack and stores `value` into `array` at `index`"""

    def execute(self):
        value, index, array = (self.peek_op_stack(i) for i in range(3))
        if array.is_null:
            return actions.throw_null_pointer()

        return IncrementProgramCounter.after(
            actions.StoreIntoArray(array=array, index=index.value, value=value),
            Pop(3)
        )


@_LOAD
class LoadFromLocals(Instructor):
    """Loads value from locals at `index_in_locals` and pushes it onto array

    If `index_in_locals` is None, the index is taken from the instruction operand.
    """

    def __init__(self, inputs, index_in_locals=None):
        super().__init__(inputs)
        if index_in_locals is not None:
            self.index_in_locals = index_in_locals
        else:
            self.index_in_locals = self.operand_as_int()

    def execute(self):
        value = self.locals.load(self.index_in_locals)
        return IncrementProgramCounter.after(
            actions.Push(value)
        )


@_LOAD_FROM_ARRAY
class LoadFromArray(Instructor):
    """Pops an `array` and an `index` from the stack and pushed the value stores in `array` at `index`"""

    def execute(self):
        index = self.peek_op_stack()
        array = self.peek_op_stack(1)
        if array.is_null:
            return actions.throw_null_pointer()

        value = array.value[index.value]
        return IncrementProgramCounter.after(
            actions.Pop(2),
            actions.Push(value)
        )
