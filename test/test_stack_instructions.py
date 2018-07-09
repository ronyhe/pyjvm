from pyjvm.actions import Pop, Push
from pyjvm.jvm_types import Integer
from test.utils import assert_incrementing_instruction, SOME_INT


def test_pop():
    assert_incrementing_instruction(
        instruction='pop',
        op_stack=[SOME_INT],
        expected=[Pop()]
    )


def test_dup():
    assert_incrementing_instruction(
        instruction='dup',
        op_stack=[SOME_INT],
        expected=[Push(SOME_INT)]
    )


def test_dup_x1():
    some_other_int = Integer.create_instance(4)
    assert_incrementing_instruction(
        instruction='dup_x1',
        op_stack=[SOME_INT, some_other_int],
        expected=[
            Pop(2),
            Push(SOME_INT),
            Push(some_other_int),
            Push(SOME_INT)
        ]
    )
