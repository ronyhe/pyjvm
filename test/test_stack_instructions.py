from pyjvm.jvm_types import Integer, Long
from test.test_utils import BlankTestMachine

ONE, TWO, THREE, FOUR = (Integer.create_instance(i) for i in range(1, 5))
LONG_ONE, LONG_TWO = (Long.create_instance(i) for i in range(1, 3))


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


def test_dup_2_first_form():
    stack_test(
        [ONE, TWO],
        'dup2',
        [ONE, TWO, ONE, TWO]
    )


def test_dup_2_second_form():
    stack_test(
        [LONG_ONE, TWO],
        'dup2',
        [LONG_ONE, LONG_ONE, TWO]
    )


def test_dup_2_x_1_first_form():
    stack_test(
        [ONE, TWO, THREE],
        'dup2_x1',
        [ONE, TWO, THREE, ONE, TWO]
    )


def test_dup_2_x_1_second_form():
    stack_test(
        [LONG_ONE, TWO, THREE],
        'dup2_x1',
        [LONG_ONE, TWO, LONG_ONE, THREE]
    )


def test_dup_2_x_2():
    case_one = (
        [ONE, TWO, THREE, FOUR],
        [ONE, TWO, THREE, FOUR, ONE, TWO]
    )
    case_two = (
        [LONG_ONE, TWO, THREE],
        [LONG_ONE, TWO, THREE, LONG_ONE]
    )
    case_three = (
        [ONE, TWO, LONG_ONE],
        [ONE, TWO, LONG_ONE, ONE, TWO]
    )
    case_four = (
        [LONG_ONE, LONG_TWO],
        [LONG_ONE, LONG_TWO, LONG_ONE]
    )
    cases = case_one, case_two, case_three, case_four
    for before, after in cases:
        stack_test(before, 'dup2_x2', after)


def test_swap():
    stack_test(
        [ONE, TWO],
        'swap',
        [TWO, ONE]
    )
