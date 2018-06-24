from pyjvm.jvm_types import Integer, Long
from test.test_utils import BlankTestMachine

ONE, TWO, THREE = (Integer.create_instance(i) for i in range(1, 4))
LONG_ONE = Long.create_instance(1)


def stack_test(before, instruction, after):
    machine = BlankTestMachine()
    stack = machine.current_op_stack()
    for item in reversed(before):
        stack.push(item)
    machine.step_instruction(instruction)

    size = len(after)
    assert stack.size() == size
    assert list(after) == list(stack.peek_many(size))


def test_pop():
    stack_test(
        [ONE],
        'pop',
        []
    )


def test_dup():
    stack_test(
        [ONE],
        'dup',
        [ONE, ONE]
    )


def test_dup_x_1():
    stack_test(
        [ONE, TWO],
        'dup_x1',
        [ONE, TWO, ONE]
    )


def test_dup_x_2_form_one():
    stack_test(
        [ONE, TWO, THREE],
        'dup_x2',
        [ONE, TWO, THREE, ONE]
    )


def test_dup_x_2_form_two():
    stack_test(
        [ONE, LONG_ONE],
        'dup_x2',
        [ONE, LONG_ONE, ONE]
    )


def test_dup_x_2_form_two_with_three_stack_elements():
    stack_test(
        [ONE, LONG_ONE, TWO],
        'dup_x2',
        [ONE, LONG_ONE, ONE, TWO]
    )
