from pyjvm.execution.execution import Executor, bytecode
from pyjvm.execution.verifiers import verify_long, verify_float, verify_double, verify_integer, verify_reference
from pyjvm.jvm_types import Integer


def _simple_store_decorator(the_class):
    specs = (
        ('i', verify_integer),
        ('l', verify_long),
        ('f', verify_float),
        ('d', verify_double),
        ('a', verify_reference)
    )

    for prefix, verifier in specs:
        null_func = bytecode(prefix + 'store', verifier)
        the_class = null_func(the_class)

        for i in range(3 + 1):  # 0-3, inclusive
            arg_func = bytecode(prefix + 'store_' + str(i), verifier, index_into_locals=i)
            the_class = arg_func(the_class)

    return the_class


@_simple_store_decorator
class StoreToLocalVariable(Executor):
    def __init__(self, instruction, machine, ensure_type, index_into_locals=None):
        super().__init__(instruction, machine)
        self.ensure_type = ensure_type
        if index_into_locals is None:
            self.index_into_locals = int(self.instruction.operands[0].value)
        else:
            self.index_into_locals = index_into_locals

    def execute(self):
        value = self.machine.current_op_stack().pop()
        self.ensure_type(value)
        self.machine.current_locals().store(self.index_into_locals, value)


@bytecode('lastore', verify_long)
@bytecode('fastore', verify_float)
@bytecode('dastore', verify_double)
@bytecode('iastore', verify_integer)
@bytecode('bastore', verify_integer)
@bytecode('castore', verify_integer)
@bytecode('sastore', verify_integer)
@bytecode('aastore', verify_reference)
class StoreValueIntoArray(Executor):
    def __init__(self, instruction, machine, ensure_type):
        super().__init__(instruction, machine)
        self.ensure_type = ensure_type

    def execute(self):
        pop = self.machine.current_op_stack().pop
        value = pop()
        index = pop()
        array_ref = pop()

        if not array_ref.type.is_array_reference:
            raise TypeError()
        if not index.type == Integer:
            raise TypeError()

        self.ensure_type(value)

        try:
            array_ref.value[index.value] = value
        except IndexError:
            raise NotImplementedError()  # ArrayIndexOutOfBoundsException
