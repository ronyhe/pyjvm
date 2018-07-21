from jawa.constants import ConstantPool

from pyjvm.actions import Push
from pyjvm.instructions import constant_instructions
from pyjvm.model.jvm_types import Integer, Double
from test.utils import assert_incrementing_instruction, constant_instruction, literal_instruction


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
        instruction=literal_instruction('bipush', value),
        expected=[
            Push(Integer.create_instance(value))
        ]
    )


def test_ldc():
    value = 5.0
    constants = ConstantPool()
    constant = constants.create_double(value)

    assert_incrementing_instruction(
        instruction=constant_instruction('ldc', constant),
        constants=constants,
        expected=[
            Push(Double.create_instance(value))
        ]
    )
