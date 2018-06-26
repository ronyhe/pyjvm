from jawa.util.bytecode import Operand, OperandTypes

from pyjvm.jvm_types import Integer
from test.test_utils import BlankTestMachine

ONE, TWO = [Integer.create_instance(i) for i in range(1, 3)]


def bin_op_test(expected, instruction, left, right):
    machine = BlankTestMachine()
    stack = machine.current_op_stack()
    stack.push(left)
    stack.push(right)
    machine.step_instruction(instruction)
    assert stack.size() == 1
    assert stack.peek() == expected


def test_simple_addition():
    bin_op_test(TWO, 'iadd', ONE, ONE)


def test_i_inc():
    machine = BlankTestMachine()
    index = 2
    locals_ = machine.current_locals()
    locals_.store(index, ONE)
    ops = Operand(OperandTypes.LOCAL_INDEX, index), Operand(OperandTypes.LITERAL, ONE.value)
    machine.step_instruction('iinc', ops)
    actual = locals_.load(index)
    assert TWO == actual
