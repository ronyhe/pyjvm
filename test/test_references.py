from jawa.constants import ConstantPool
from jawa.util.bytecode import Instruction, Operand, OperandTypes

from pyjvm.actions import Push
from pyjvm.jvm_class import JvmObject
from pyjvm.jvm_types import Integer, NULL_VALUE
from test.utils import assert_incrementing_instruction, DUMMY_CLASS, assert_instruction


def test_instance_of():
    class_name = DUMMY_CLASS.name
    consts = ConstantPool()
    const = consts.create_class(class_name)
    instruction = Instruction.create('instanceof', [Operand(OperandTypes.CONSTANT_INDEX, const.index)])
    obj = DUMMY_CLASS.type.create_instance(JvmObject(dict()))

    assert_incrementing_instruction(
        instruction=instruction,

        constants=consts,

        op_stack=[obj],

        expected=[
            Push(Integer.create_instance(1))
        ]
    )


def test_null_instance_of():
    class_name = DUMMY_CLASS.name
    consts = ConstantPool()
    const = consts.create_class(class_name)
    instruction = Instruction.create('instanceof', [Operand(OperandTypes.CONSTANT_INDEX, const.index)])
    obj = NULL_VALUE

    assert_instruction(
        instruction=instruction,

        constants=consts,

        op_stack=[obj],

        expected=[
            Push(Integer.create_instance(0))
        ]
    )
