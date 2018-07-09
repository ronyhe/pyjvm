from pyjvm.actions import Pop
from test.utils import assert_incrementing_instruction, SOME_INT


def test_pop():
    assert_incrementing_instruction(
        instruction='pop',
        op_stack=[SOME_INT],
        expected=[Pop()]
    )
