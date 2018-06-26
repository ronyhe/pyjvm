from pyjvm.jvm_types import Integer, Long, Float
from test.test_utils import BlankTestMachine


def conversion_test(source, instruction, target):
    machine = BlankTestMachine()
    stack = machine.current_op_stack()
    stack.push(source)
    machine.step_instruction(instruction)
    assert stack.size() == 1
    assert stack.peek() == target


def test_int_to_long():
    conversion_test(
        Integer.create_instance(1),
        'i2l',
        Long.create_instance(1)
    )


def test_int_to_float():
    conversion_test(
        Integer.create_instance(1),
        'i2f',
        Float.create_instance(1)
    )
