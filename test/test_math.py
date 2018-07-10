from pyjvm.actions import Pop, Push
from pyjvm.instructions.math import OPERATORS
from test.utils import assert_incrementing_instruction


def test_math():
    left = 6
    right = 3
    for binary in OPERATORS:
        for name, args in binary.bytecode_args().items():
            op, type_ = args
            assert_incrementing_instruction(
                instruction=name,
                op_stack=[type_.create_instance(right), type_.create_instance(left)],
                expected=[
                    Pop(2),
                    Push(type_.create_instance(op(left, right)))
                ]
            )
