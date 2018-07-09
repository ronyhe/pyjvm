from pyjvm.actions import Pop, Push, PushMany
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
            PushMany([
                SOME_INT,
                some_other_int,
                SOME_INT
            ])
        ]
    )


def test_dup_x2_first_form():
    first, second, third = (Integer.create_instance(i) for i in range(3))
    assert_incrementing_instruction(
        instruction='dup_x2',
        op_stack=[first, second, third],
        expected=[
            Pop(3),
            PushMany([
                first, second, third, first
            ])
        ]
    )
