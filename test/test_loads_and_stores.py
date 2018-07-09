from jawa.util.bytecode import Instruction, Operand, OperandTypes

from pyjvm.actions import StoreInLocals, Pop, StoreIntoArray, Push
from pyjvm.frame_locals import Locals
from pyjvm.jvm_types import ArrayReferenceType, Integer
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
        instruction='istore_2',

        op_stack=[SOME_INT],

        expected=[
            StoreInLocals(index=2, value=SOME_INT),
            Pop
        ]
    )


def test_int_store_into_array():
    value = SOME_INT
    index = Integer.create_instance(1)
    array = ArrayReferenceType(Integer).create_instance([0])

    assert_incrementing_instruction(
        instruction='iastore',

        op_stack=[value, index, array],

        expected=[
            StoreIntoArray(array=array, index=index.value, value=value),
            Pop(3)
        ]
    )


def test_int_load():
    locals_ = Locals(5)
    locals_.store(2, SOME_INT)
    assert_incrementing_instruction(
        instruction='iload_2',
        locals=locals_,
        expected=[
            Push(SOME_INT)
        ]
    )
