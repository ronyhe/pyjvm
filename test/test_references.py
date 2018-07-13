from jawa.constants import ConstantPool
from jawa.util.bytecode import Instruction, Operand, OperandTypes

from pyjvm.actions import Push, ThrowNullPointerException
from pyjvm.jvm_class import JvmObject
from pyjvm.jvm_types import Integer, NULL_VALUE, ArrayReferenceType
from test.utils import assert_incrementing_instruction, DUMMY_CLASS, assert_instruction

TRUE = Integer.create_instance(1)
FALSE = Integer.create_instance(0)


def test_instance_of():
    class_name = DUMMY_CLASS.name
    consts = ConstantPool()
    const = consts.create_class(class_name)
    instruction = Instruction.create('instanceof', [Operand(OperandTypes.CONSTANT_INDEX, const.index)])
    obj = DUMMY_CLASS.type.create_instance(JvmObject(dict()))

    args = {
        'instruction': instruction,
        'constants': consts
    }

    assert_incrementing_instruction(
        op_stack=[obj],
        expected=[
            Push(TRUE)
        ],
        **args
    )

    assert_incrementing_instruction(
        op_stack=[NULL_VALUE],
        expected=[
            Push(FALSE)
        ],
        **args
    )


def test_array_length():
    size = 54
    items = [Integer.create_instance(1) for _ in range(size)]
    array = ArrayReferenceType(Integer).create_instance(items)
    assert_incrementing_instruction(
        instruction='arraylength',
        op_stack=[array],
        expected=[
            Push(Integer.create_instance(size))
        ]
    )


def test_null_array_length():
    assert_instruction(
        instruction='arraylength',
        op_stack=[NULL_VALUE],
        expected=[
            ThrowNullPointerException
        ]
    )
