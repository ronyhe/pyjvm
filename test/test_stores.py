from jawa.util.bytecode import Instruction, Operand, OperandTypes

from pyjvm.actions import StoreInLocals, Pop, IncrementProgramCounter
from pyjvm.instructions.instructions import execute_instruction
from pyjvm.jvm_types import Integer
from pyjvm.stack import Stack
from test.utils import DefaultInputs


def test_int_store():
    index = 1
    value = Integer.create_instance(6)

    instruction = Instruction.create('istore', [Operand(OperandTypes.LITERAL, index)])
    inputs = DefaultInputs(instruction=instruction, op_stack=Stack([value]))

    actions = execute_instruction(inputs)
    assert actions.has(
        StoreInLocals(value=value, index=index),
        Pop(),
        IncrementProgramCounter
    )
