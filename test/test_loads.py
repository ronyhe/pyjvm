from jawa.cf import ClassFile
from jawa.util.bytecode import Instruction, Operand, OperandTypes

from pyjvm.machine import Frame, Machine
from pyjvm.stack import Stack
from pyjvm.values import Locals, Value, ImpType


def blank_test_machine():
    frame = Frame(Locals(5), Stack(), [], 0)
    frames = Stack()
    frames.push(frame)
    # noinspection PyTypeChecker
    return Machine(ClassFile.create('TestClass'), frames, None)


def test_iload():
    integer_value = 6
    local_index = 0
    machine = blank_test_machine()
    index_constant = machine.current_class.constants.create_integer(local_index)
    instruction = Instruction.create('iload', [Operand(OperandTypes.CONSTANT_INDEX, index_constant.index)])

    machine.current_locals().store(local_index, Value(ImpType.integer(), integer_value))
    machine.instruction = instruction
    machine.step()

    assert machine.current_op_stack().peek() == Value(ImpType.integer(), integer_value)
