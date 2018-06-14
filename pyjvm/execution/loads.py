from jawa import constants
from jawa.cf import ClassFile
from jawa.util.bytecode import Instruction, Operand, OperandTypes

from pyjvm.execution.execution import Executor
from pyjvm.machine import Machine, Frame
from pyjvm.stack import Stack
from pyjvm.values import ImpTypes, Locals, Value


# noinspection PyPep8Naming,SpellCheckingInspection
class iload(Executor):
    """Load int from local variable"""
    def execute(self, instruction, machine):
        index_of_int_in_locals = self._get_index_of_int_in_locals(instruction, machine)

        value_at_index = machine.current_locals().load(index_of_int_in_locals)

        if not value_at_index.imp_type == ImpTypes.Integer:
            raise TypeError()

        machine.current_op_stack().push(value_at_index)

    # noinspection PyMethodMayBeStatic
    def _get_index_of_int_in_locals(self, instruction, machine):
        constant_index = instruction.operands[0].value
        constant = machine.current_constants()[constant_index]

        if not isinstance(constant, constants.Integer):
            raise TypeError()

        return constant.value

    # noinspection PyMethodMayBeStatic
    def test(self):
        the_class = ClassFile()
        index_constant = the_class.constants.create_integer(0)
        instruction = Instruction.create('iload', [Operand(OperandTypes.CONSTANT_INDEX, index_constant.index)])
        _locals = Locals(1)
        _locals.store(0, Value(ImpTypes.Integer, 6))
        frame = Frame(_locals, Stack(), [], 0)
        frames = Stack()
        frames.push(frame)
        machine = Machine(the_class, frames, instruction)
        machine.step()
        assert machine.current_op_stack().peek() == Value(ImpTypes.Integer, 6)
