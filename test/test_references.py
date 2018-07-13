from jawa.constants import ConstantPool
from jawa.util.bytecode import Instruction, Operand, OperandTypes

from pyjvm import value_array_type_indicators
from pyjvm.actions import Push, ThrowNullPointerException, Pop, ThrowNegativeArraySizeException, ThrowCheckCastException
from pyjvm.jvm_class import JvmObject
from pyjvm.jvm_types import Integer, NULL_VALUE, ArrayReferenceType
from test.utils import assert_incrementing_instruction, DUMMY_CLASS, assert_instruction, DUMMY_SUB_CLASS_NAME

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


def test_check_cast():
    class_name = DUMMY_CLASS.name
    consts = ConstantPool()
    const = consts.create_class(class_name)
    instruction = Instruction.create('checkcast', [Operand(OperandTypes.CONSTANT_INDEX, const.index)])
    obj = DUMMY_CLASS.type.create_instance(JvmObject(dict()))

    assert_incrementing_instruction(
        constants=consts,
        instruction=instruction,
        op_stack=[obj],
        expected=[]
    )


def test_check_null_cast():
    class_name = DUMMY_CLASS.name
    consts = ConstantPool()
    const = consts.create_class(class_name)
    instruction = Instruction.create('checkcast', [Operand(OperandTypes.CONSTANT_INDEX, const.index)])

    assert_incrementing_instruction(
        constants=consts,
        instruction=instruction,
        op_stack=[NULL_VALUE],
        expected=[]
    )


def test_negative_check_cast():
    class_name = DUMMY_SUB_CLASS_NAME
    consts = ConstantPool()
    const = consts.create_class(class_name)
    instruction = Instruction.create('checkcast', [Operand(OperandTypes.CONSTANT_INDEX, const.index)])
    obj = DUMMY_CLASS.type.create_instance(JvmObject(dict()))

    assert_instruction(
        constants=consts,
        instruction=instruction,
        op_stack=[obj],
        expected=[ThrowCheckCastException]
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


def test_new_value_type_array():
    type_ = Integer
    indicator = value_array_type_indicators.indicator_by_type(type_)
    instruction = Instruction.create('newarray', [Operand(OperandTypes.LITERAL, indicator)])
    size = 34
    expected_value = [type_.create_instance(type_.default_value) for _ in range(size)]
    expected_object = ArrayReferenceType(type_).create_instance(expected_value)
    assert_incrementing_instruction(
        instruction=instruction,
        op_stack=[Integer.create_instance(size)],
        expected=[
            Pop(),
            Push(expected_object)
        ]
    )


def test_new_ref_array():
    type_ = DUMMY_CLASS.type
    class_name = DUMMY_CLASS.name
    consts = ConstantPool()
    const = consts.create_class(class_name)
    instruction = Instruction.create('anewarray', [Operand(OperandTypes.CONSTANT_INDEX, const.index)])

    size = 43
    expected_value = [type_.create_instance(type_.default_value) for _ in range(size)]
    expected_object = ArrayReferenceType(type_).create_instance(expected_value)

    assert_incrementing_instruction(
        instruction=instruction,
        constants=consts,
        op_stack=[Integer.create_instance(size)],
        expected=[
            Pop(),
            Push(expected_object)
        ]
    )


def test_negative_array_size():
    type_ = Integer
    indicator = value_array_type_indicators.indicator_by_type(type_)
    instruction = Instruction.create('newarray', [Operand(OperandTypes.LITERAL, indicator)])
    assert_instruction(
        instruction=instruction,
        op_stack=[Integer.create_instance(-4)],
        expected=[
            ThrowNegativeArraySizeException
        ]
    )
