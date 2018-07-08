from jawa.util.bytecode import Instruction, Operand, OperandTypes

from pyjvm.actions import StoreInLocals, Pop, IncrementProgramCounter
from pyjvm.jvm_types import Integer
from pyjvm.stack import Stack
from test.utils import assert_instruction


def test_int_store_():
    index = 1
    value = Integer.create_instance(6)
    instruction = Instruction.create('istore', [Operand(OperandTypes.LITERAL, index)])

    assert_instruction(
        instruction=instruction,
        op_stack=Stack([value]),
        expected=[
            StoreInLocals(value=value, index=index),
            Pop(),
            IncrementProgramCounter
        ]
    )
