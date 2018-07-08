from pyjvm.instructions.instructions import Instructor, bytecode
from pyjvm.instructions.old_instructions.verifiers import verify_integer, verify_long, verify_double, verify_float, \
    verify_reference, \
    verify_array_reference


def _load_from_locals_decorator(the_class):
    specs = (
        ('i', verify_integer),
        ('l', verify_long),
        ('d', verify_double),
        ('f', verify_float),
        ('a', verify_reference)
    )

    for letter, verifier in specs:
        no_index_name = letter + 'load'
        the_class = bytecode(no_index_name, verifier)(the_class)
        for i in range(3 + 1):
            name = letter + 'load_' + str(i)
            the_class = bytecode(name, verifier, i)(the_class)

    return the_class


@_load_from_locals_decorator
class LoadFromLocals(Instructor):
    def __init__(self, instruction, machine, ensure_type, index_in_locals=None):
        super().__init__(instruction, machine)
        self.ensure_type = ensure_type
        self.index_in_locals = index_in_locals

    def execute(self):
        if self.index_in_locals is None:
            index = int(self.instruction.operands[0].value)
        else:
            index = self.index_in_locals

        value = self.machine.current_locals().load(index)
        self.ensure_type(value)
        self.machine.current_op_stack().push(value)


# noinspection SpellCheckingInspection
@bytecode('laload', verify_long)
@bytecode('faload', verify_float)
@bytecode('daload', verify_double)
@bytecode('iaload', verify_integer)
@bytecode('baload', verify_integer)
@bytecode('caload', verify_integer)
@bytecode('saload', verify_integer)
@bytecode('aaload', verify_reference)
class LoadFromArray(Instructor):
    def __init__(self, instruction, machine, ensure_type):
        super().__init__(instruction, machine)
        self.ensure_type = ensure_type

    def execute(self):
        stack = self.machine.current_op_stack()
        index = stack.pop()
        array_ref = stack.pop()

        verify_integer(index)
        verify_array_reference(array_ref)

        if array_ref.is_null:
            raise NotImplementedError()  # NullReferenceException

        try:
            value = array_ref.value[index.value]
        except IndexError:
            raise NotImplementedError()  # ArrayIndexOutOfBoundException
        else:
            self.ensure_type(value)
            stack.push(value)
