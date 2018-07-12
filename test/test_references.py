from jawa.constants import ConstantPool
from jawa.util.bytecode import Instruction, Operand, OperandTypes

from pyjvm.actions import Push
from pyjvm.jvm_class import JvmObject
from pyjvm.jvm_types import Integer, NULL_VALUE
from test.utils import assert_incrementing_instruction, DUMMY_CLASS


def test_instance_of():
    class_name = DUMMY_CLASS.name
    consts = ConstantPool()
    const = consts.create_class(class_name)
    instruction = Instruction.create('instanceof', [Operand(OperandTypes.CONSTANT_INDEX, const.index)])
    obj = DUMMY_CLASS.type.create_instance(JvmObject(dict()))

    true = Integer.create_instance(1)
    false = Integer.create_instance(0)

    args = {
        'instruction': instruction,
        'constants': consts
    }

    assert_incrementing_instruction(
        op_stack=[obj],
        expected=[
            Push(true)
        ],
        **args
    )

    assert_incrementing_instruction(
        op_stack=[NULL_VALUE],
        expected=[
            Push(false)
        ],
        **args
    )
