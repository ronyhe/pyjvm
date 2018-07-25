from jawa.util.bytecode import Instruction

from pyjvm.actions import Pop, Push
from pyjvm.instructions.math import OPERATORS
from pyjvm.model.frame_locals import Locals
from pyjvm.model.jvm_types import Integer
from pyjvm.utils.utils import local_operand, literal_operand
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
    original_value = 8
    local_index = 2
    amount_to_add = 5

    locals_ = Locals(local_index + 1)
    locals_.store(local_index, Integer.create_instance(original_value))

    instruction = Instruction.create('iinc', [
        local_operand(local_index),
        literal_operand(amount_to_add)
    ])

    assert_incrementing_instruction(
        instruction=instruction,
        locals=locals_,
        expected=[
            Push(Integer.create_instance(original_value + amount_to_add))
        ]
    )
