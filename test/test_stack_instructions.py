from pyjvm.jvm_types import Integer
from test.test_utils import BlankTestMachine


def test_pop():
    machine = BlankTestMachine()
    stack = machine.current_op_stack()
    stack.push(Integer.create_instance(1))
    machine.step_instruction('pop')
    assert stack.size() == 0
