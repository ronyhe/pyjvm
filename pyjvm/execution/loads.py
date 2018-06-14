from jawa import constants

from pyjvm.execution.execution import Executor
from pyjvm.values import ImpTypes


# noinspection PyPep8Naming,SpellCheckingInspection
class iload(Executor):
    def execute(self, instruction, machine):
        constant_index = instruction.operands[0].value
        constant = machine.current_constants()[constant_index]
        if not isinstance(constant, constants.Integer):
            raise TypeError()

        local_index = constant.value
        value_at_index = machine.current_locals().load(local_index)

        if not value_at_index.imp_type == ImpTypes.Integer:
            raise TypeError()

        machine.current_op_stack().push(value_at_index)
