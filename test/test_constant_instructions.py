from jawa.constants import ConstantPool
from jawa.util.bytecode import Instruction, Operand, OperandTypes

from pyjvm.actions import Push
from pyjvm.instructions import constant_instructions
from pyjvm.jvm_types import Integer, Double
from test.utils import assert_incrementing_instruction


def _constant_test(mnemonic, value):
    assert_incrementing_instruction(
        instruction=mnemonic,
        expected=[
            Push(value)
        ]
    )


def _constant_tests(pairs):
    for name, value in dict(pairs).items():
        _constant_test(name, value)


def test_constants():
    _constant_tests(constant_instructions.CONSTANT_VALUES)


def test_bipush():
    value = 5
    assert_incrementing_instruction(
        instruction=Instruction.create('bipush', [Operand(OperandTypes.LITERAL, value)]),
        expected=[
            Push(Integer.create_instance(value))
        ]
    )


def test_ldc():
    value = 5.0
    constants = ConstantPool()
    constant = constants.create_double(value)
    instruction = Instruction.create('ldc', [Operand(OperandTypes.CONSTANT_INDEX, constant.index)])
    assert_incrementing_instruction(
        instruction=instruction,
        constants=constants,
        expected=[
            Push(Double.create_instance(value))
        ]
    )
