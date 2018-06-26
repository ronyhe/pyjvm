from pyjvm.jvm_types import Integer
from test.test_utils import BlankTestMachine


def bin_op_test(expected, instruction, left, right):
    machine = BlankTestMachine()
    stack = machine.current_op_stack()
    stack.push(left)
    stack.push(right)
    machine.step_instruction(instruction)
    assert stack.size() == 1
    assert stack.peek() == expected


def test_simple_addition():
    one, two = [Integer.create_instance(i) for i in range(1, 3)]
    bin_op_test(two, 'iadd', one, one)
