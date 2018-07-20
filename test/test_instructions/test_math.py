from pyjvm.actions import Pop, Push
from pyjvm.instructions.math import OPERATORS
from pyjvm.jvm_types import Integer
from test.utils import assert_incrementing_instruction


def test_binary_math():
    left = 6
    right = 3
    for operator in OPERATORS:
        if not operator.operands == 2:
            continue
        for name, args in operator.bytecode_args().items():
            op, type_, _ = args
            assert_incrementing_instruction(
                instruction=name,
                op_stack=[type_.create_instance(right), type_.create_instance(left)],
                expected=[
                    Pop(2),
                    Push(type_.create_instance(op(left, right)))
                ]
            )


def test_neg():
    assert_incrementing_instruction(
        instruction='ineg',
        op_stack=[Integer.create_instance(3)],
        expected=[
            Pop(),
            Push(Integer.create_instance(-3))
        ]
    )


def test_iinc():
    assert_incrementing_instruction(
        instruction='iinc',
        op_stack=[Integer.create_instance(2)],
        expected=[
            Pop(),
            Push(Integer.create_instance(3))
        ]
    )
