from pyjvm.actions import StoreInLocals, Pop, StoreIntoArray, Push, throw_null_pointer
from pyjvm.core.frame_locals import Locals
from pyjvm.core.jvm_types import ArrayReferenceType, Integer, NULL_VALUE
from test.utils import SOME_INT, assert_incrementing_instruction, assert_instruction, literal_instruction


def test_int_store():
    index = 1

    assert_incrementing_instruction(
        instruction=literal_instruction('istore', index),

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


def test_int_store_into_null_array():
    value = SOME_INT
    index = Integer.create_instance(1)
    array = NULL_VALUE

    assert_instruction(
        instruction='iastore',

        op_stack=[value, index, array],

        expected=[
            throw_null_pointer()
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


def test_int_load_from_array():
    array = ArrayReferenceType(Integer).create_instance([SOME_INT])
    index = Integer.create_instance(0)
    assert_incrementing_instruction(
        instruction='iaload',

        op_stack=[index, array],

        expected=[
            Pop(2),
            Push(SOME_INT)
        ]
    )


def test_int_load_from_null_array():
    array = NULL_VALUE
    index = Integer.create_instance(0)
    assert_instruction(
        instruction='iaload',

        op_stack=[index, array],

        expected=[
            throw_null_pointer()
        ]
    )
