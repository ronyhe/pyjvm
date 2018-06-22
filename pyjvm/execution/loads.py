from jawa import constants

from pyjvm.execution.execution import Executor, bytecode
from pyjvm.jvm_class import Integer


@bytecode('iload')
@bytecode('iload_0', 0)
@bytecode('iload_1', 1)
@bytecode('iload_2', 2)
@bytecode('iload_3', 3)
class IntLoad(Executor):
    def __init__(self, instruction, machine, index=None):
        super().__init__(instruction, machine)
        self.index = index

    def execute(self):
        if self.index is None:
            self.index = self._get_index_of_int_in_locals()

        _load_from_locals(self.machine, self.index, ensure_type=Integer)

    def _get_index_of_int_in_locals(self):
        constant_index = self.instruction.operands[0].value
        constant = self.machine.current_constants()[constant_index]

        if not isinstance(constant, constants.Integer):
            raise TypeError()

        return constant.value


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
