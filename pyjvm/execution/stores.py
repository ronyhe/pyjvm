from pyjvm.execution.execution import Executor, bytecode
from pyjvm.types import Integer, Long, Float, Double


def _simple_store_decorator(the_class):
    specs = (
        (Integer, 'i'),
        (Long, 'l'),
        (Float, 'f'),
        (Double, 'd')
    )

    for type_, prefix in specs:
        null_func = bytecode(prefix + 'store', ensure_type=type_)
        the_class = null_func(the_class)

        for i in range(3 + 1):  # 0-3, inclusive
            arg_func = bytecode(prefix + 'store_' + str(i), index_into_locals=i, ensure_type=type_)
            the_class = arg_func(the_class)

    return the_class


@bytecode('astore')
@_simple_store_decorator
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


@bytecode('lastore', Long)
@bytecode('fastore', Float)
@bytecode('dastore', Double)
@bytecode('iastore', Integer)
@bytecode('bastore', Integer)
@bytecode('castore', Integer)
@bytecode('sastore', Integer)
@bytecode('aastore')
class StoreValueIntoArray(Executor):
    def __init__(self, instruction, machine, ensure_type=None):
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
        if self.ensure_type is not None and not self.ensure_type == value.type:
            raise TypeError()

        try:
            array_ref.value[index.value] = value
        except IndexError:
            raise NotImplementedError()  # ArrayIndexOutOfBoundsException
