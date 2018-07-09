from jawa.util.bytecode import Instruction, Operand, OperandTypes

from pyjvm.actions import StoreInLocals, Pop
from test.utils import SOME_INT, assert_incrementing_instruction


def test_int_store():
    index = 1
    instruction = Instruction.create('istore', [Operand(OperandTypes.LITERAL, index)])

    assert_incrementing_instruction(
        instruction=instruction,

        op_stack=[SOME_INT],

        expected=[
            StoreInLocals(value=SOME_INT, index=index),
            Pop,
        ]
    )


def test_int_store_with_built_in_index():
    assert_incrementing_instruction(
        instruction=Instruction.create('istore_2'),

        op_stack=[SOME_INT],

        expected=[
            StoreInLocals(index=2, value=SOME_INT),
            Pop
        ]
    )
