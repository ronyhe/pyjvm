from pyjvm.actions import Pop, Push
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

