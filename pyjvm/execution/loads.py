from pyjvm.execution.execution import Executor, bytecode
from pyjvm.execution.verifiers import verify_integer, verify_long, verify_double, verify_float, verify_reference
from pyjvm.types import Integer


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
class LoadFromLocals(Executor):
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


@bytecode('aaload')
class AALoad(Executor):
    def execute(self):
        stack = self.machine.current_op_stack()
        index = stack.pop()
        array_ref = stack.pop()

        if not index.type == Integer:
            raise TypeError()

        if not array_ref.type.is_array_reference:
            raise TypeError()

        if array_ref.is_null:
            raise NotImplementedError()  # NullPointerException

        try:
            value = array_ref.value[index.value]
        except IndexError:
            raise NotImplementedError()  # ArrayIndexOutOfBoundsException
        else:
            stack.push(value)


def _load_from_locals(machine, index_in_locals, ensure_type=None):
    local = machine.current_locals().load(index_in_locals)

    if ensure_type is not None and not local.type == ensure_type:
        raise TypeError()

    machine.current_op_stack().push(local)


def _load_integer_from_locals(machine, index_in_locals):
    return _load_from_locals(machine, index_in_locals, ensure_type=Integer)
