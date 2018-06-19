from jawa import constants

from pyjvm.execution.execution import Executor
from pyjvm.values import BaseType


def _load_from_locals(machine, index_in_locals, base_type=None):
    local = machine.current_locals().load(index_in_locals)

    if base_type is not None and not local.imp_type.base == base_type:
        raise TypeError()

    machine.current_op_stack().push(local)


def _load_integer_from_locals(machine, index_in_locals):
    return _load_from_locals(machine, index_in_locals, base_type=BaseType.Integer)


class iload(Executor):
    """Load int from local variable"""

    def execute(self, instruction, machine):
        index_of_int_in_locals = self._get_index_of_int_in_locals(instruction, machine)
        _load_integer_from_locals(machine, index_of_int_in_locals)

    def _get_index_of_int_in_locals(self, instruction, machine):
        constant_index = instruction.operands[0].value
        constant = machine.current_constants()[constant_index]

        if not isinstance(constant, constants.Integer):
            raise TypeError()

        return constant.value

class iload_0(Executor):
    def execute(self, instruction, machine):
        _load_integer_from_locals(machine, 0)


class iload_1(Executor):
    def execute(self, instruction, machine):
        _load_integer_from_locals(machine, 1)


class iload_2(Executor):
    def execute(self, instruction, machine):
        _load_integer_from_locals(machine, 2)


class iload_3(Executor):
    def execute(self, instruction, machine):
        _load_integer_from_locals(machine, 3)
