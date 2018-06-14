from jawa import constants
from jawa.cf import ClassFile
from jawa.util.bytecode import Instruction, Operand, OperandTypes

from pyjvm.execution.execution import Executor
from pyjvm.machine import Machine, Frame
from pyjvm.stack import Stack
from pyjvm.values import ImpTypes, Locals, Value


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
