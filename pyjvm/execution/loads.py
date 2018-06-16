from jawa import constants
from jawa.util.bytecode import Instruction, Operand, OperandTypes

from pyjvm.execution.execution import Executor
from pyjvm.values import ImpTypes, Value


def _load_from_locals(machine, index_in_locals, imp_type=None):
    local = machine.current_locals().load(index_in_locals)

    if imp_type is not None and not local.imp_type == imp_type:
        raise TypeError()

    machine.current_op_stack().push(local)


class iload(Executor):
    """Load int from local variable"""
    def execute(self, instruction, machine):
        index_of_int_in_locals = self._get_index_of_int_in_locals(instruction, machine)
        _load_from_locals(machine, index_of_int_in_locals, ImpTypes.Integer)

    def _get_index_of_int_in_locals(self, instruction, machine):
        constant_index = instruction.operands[0].value
        constant = machine.current_constants()[constant_index]

        if not isinstance(constant, constants.Integer):
            raise TypeError()

        return constant.value

    def test(self, machine):
        integer_value = 6
        local_index = 0

        index_constant = machine.current_class.constants.create_integer(local_index)
        instruction = Instruction.create('iload', [Operand(OperandTypes.CONSTANT_INDEX, index_constant.index)])

        machine.current_locals().store(local_index, Value(ImpTypes.Integer, integer_value))
        machine.instruction = instruction
        machine.step()

        assert machine.current_op_stack().peek() == Value(ImpTypes.Integer, integer_value)


class iload_0(Executor):
    def execute(self, instruction, machine):
        _load_from_locals(machine, 0, ImpTypes.Integer)


class iload_1(Executor):
    def execute(self, instruction, machine):
        _load_from_locals(machine, 1, ImpTypes.Integer)


class iload_2(Executor):
    def execute(self, instruction, machine):
        _load_from_locals(machine, 2, ImpTypes.Integer)


class iload_3(Executor):
    def execute(self, instruction, machine):
        _load_from_locals(machine, 3, ImpTypes.Integer)
