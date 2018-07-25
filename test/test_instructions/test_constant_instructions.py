from jawa.constants import ConstantPool

from pyjvm.actions import Push
from pyjvm.instructions import constant_instructions
from pyjvm.model.jvm_class import JvmObject
from pyjvm.model.jvm_types import Integer, Double, ObjectReferenceType, ArrayReferenceType
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


def test_string_constant():
    text = 'some_text'
    consts = ConstantPool()
    const = consts.create_string(text)

    chars = [ord(c) for c in text]
    char_array = ArrayReferenceType(Integer).create_instance(chars)
    hash_value = hash(text) % (2 ** 32)
    hash_ = Integer.create_instance(hash_value)

    reference_type = ObjectReferenceType('java/lang/String')
    jvm_object = JvmObject({
        'hash': hash_,
        'value': char_array
    })

    assert_incrementing_instruction(
        instruction=constant_instruction('ldc', const),
        constants=consts,
        expected=[
            Push(
                reference_type.create_instance(jvm_object)
            )
        ]
    )
