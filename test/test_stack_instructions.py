from pyjvm.jvm_types import Integer
from test.test_utils import BlankTestMachine


def test_pop():
    machine = BlankTestMachine()
    stack = machine.current_op_stack()
    stack.push(Integer.create_instance(1))
    machine.step_instruction('pop')
    assert stack.size() == 0


def test_dup():
    machine = BlankTestMachine()
    stack = machine.current_op_stack()
    stack.push(Integer.create_instance(1))
    machine.step_instruction('dup')
    assert stack.size() == 2
    assert stack.pop() == stack.pop()


def test_dup_x_1():
    machine = BlankTestMachine()
    stack = machine.current_op_stack()
    stack.push(Integer.create_instance(1))
    stack.push(Integer.create_instance(2))
    machine.step_instruction('dup_x1')
    assert stack.size() == 3
    first, _, third = (stack.pop() for _ in range(3))
    assert first == third
