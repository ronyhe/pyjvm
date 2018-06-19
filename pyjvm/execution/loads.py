from jawa import constants

from pyjvm.execution.execution import Executor, bytecode
from pyjvm.values import BaseType


def _load_from_locals(machine, index_in_locals, base_type=None):
    local = machine.current_locals().load(index_in_locals)

    if base_type is not None and not local.imp_type.base == base_type:
        raise TypeError()

    machine.current_op_stack().push(local)


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

        _load_from_locals(self.machine, self.index, base_type=BaseType.Integer)

    def _get_index_of_int_in_locals(self):
        constant_index = self.instruction.operands[0].value
        constant = self.machine.current_constants()[constant_index]

        if not isinstance(constant, constants.Integer):
            raise TypeError()

        return constant.value


def _load_integer_from_locals(machine, index_in_locals):
    return _load_from_locals(machine, index_in_locals, base_type=BaseType.Integer)
