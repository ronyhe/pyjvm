from jawa.constants import ConstantPool

from pyjvm import value_array_type_indicators
from pyjvm.actions import Push, ThrowNullPointerException, Pop, ThrowNegativeArraySizeException, \
    ThrowCheckCastException, ThrowObject, PushNewInstance, PutField, PutStatic
from pyjvm.jawa_conversions import convert_class_file
from pyjvm.jvm_class import JvmObject
from pyjvm.jvm_types import Integer, NULL_VALUE, ArrayReferenceType
from pyjvm.utils import TRUE, FALSE
from test.utils import assert_incrementing_instruction, DUMMY_CLASS, assert_instruction, DUMMY_SUB_CLASS_NAME, \
    constant_instruction, literal_instruction, dummy_loader


def test_instance_of():
    class_name = DUMMY_CLASS.name
    consts = ConstantPool()
    const = consts.create_class(class_name)
    instruction = constant_instruction('instanceof', const)
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
    obj = DUMMY_CLASS.type.create_instance(JvmObject(dict()))

    assert_incrementing_instruction(
        constants=consts,
        instruction=constant_instruction('checkcast', const),
        op_stack=[obj],
        expected=[]
    )


def test_check_null_cast():
    class_name = DUMMY_CLASS.name
    consts = ConstantPool()
    const = consts.create_class(class_name)

    assert_incrementing_instruction(
        constants=consts,
        instruction=constant_instruction('checkcast', const),
        op_stack=[NULL_VALUE],
        expected=[]
    )


def test_negative_check_cast():
    class_name = DUMMY_SUB_CLASS_NAME
    consts = ConstantPool()
    const = consts.create_class(class_name)
    obj = DUMMY_CLASS.type.create_instance(JvmObject(dict()))

    assert_instruction(
        constants=consts,
        instruction=constant_instruction('checkcast', const),
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
    size = 34
    expected_value = [type_.create_instance(type_.default_value) for _ in range(size)]
    expected_object = ArrayReferenceType(type_).create_instance(expected_value)

    assert_incrementing_instruction(
        instruction=literal_instruction('newarray', indicator),
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

    size = 43
    expected_value = [type_.create_instance(type_.default_value) for _ in range(size)]
    expected_object = ArrayReferenceType(type_).create_instance(expected_value)

    assert_incrementing_instruction(
        instruction=constant_instruction('anewarray', const),
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
    assert_instruction(
        instruction=literal_instruction('newarray', indicator),
        op_stack=[Integer.create_instance(-4)],
        expected=[
            ThrowNegativeArraySizeException
        ]
    )


def test_a_throw():
    obj = DUMMY_CLASS.type.create_instance(JvmObject(dict()))
    assert_instruction(
        instruction='athrow',
        op_stack=[obj],
        expected=[
            ThrowObject(obj)
        ]
    )


def test_new():
    consts = ConstantPool()
    const = consts.create_class(DUMMY_CLASS.name)
    class_ = convert_class_file(DUMMY_CLASS.class_file)

    assert_incrementing_instruction(
        constants=consts,
        instruction=constant_instruction('new', const),
        expected=[
            PushNewInstance(class_)
        ]
    )


def test_get_field():
    consts = ConstantPool()
    field_ref = DUMMY_CLASS.instance_field_ref(consts)

    value = Integer.create_instance(50)
    fields = {
        DUMMY_CLASS.instance_field.name: value
    }
    obj = DUMMY_CLASS.type.create_instance(JvmObject(fields))

    assert_incrementing_instruction(
        instruction=constant_instruction('getfield', field_ref),
        constants=consts,
        op_stack=[obj],
        expected=[
            Pop(),
            Push(value)
        ]
    )


def test_put_field():
    consts = ConstantPool()
    field_ref = DUMMY_CLASS.instance_field_ref(consts)

    value = Integer.create_instance(50)
    fields = {
        DUMMY_CLASS.instance_field.name: Integer.create_instance(Integer.default_value)
    }
    obj = DUMMY_CLASS.type.create_instance(JvmObject(fields))

    assert_incrementing_instruction(
        instruction=constant_instruction('putfield', field_ref),
        constants=consts,
        op_stack=[value, obj],
        expected=[
            Pop(2),
            PutField(obj, DUMMY_CLASS.instance_field.name.value, value)
        ]
    )


def test_put_static():
    consts = ConstantPool()
    field_ref = DUMMY_CLASS.class_field_ref(consts)
    value = Integer.create_instance(45)
    assert_incrementing_instruction(
        constants=consts,
        instruction=constant_instruction('putstatic', field_ref),
        op_stack=[value],
        expected=[
            Pop(),
            PutStatic(field_ref.class_.name.value, field_ref.name_and_type.name.value.value, value)
        ]
    )


def test_get_static():
    class_name = DUMMY_CLASS.name
    field_name = DUMMY_CLASS.class_field.name.value
    loader = dummy_loader()
    consts = ConstantPool()

    value = Integer.create_instance(67)
    loader.get_the_statics(class_name)[field_name] = value
    field_ref = DUMMY_CLASS.class_field_ref(consts)

    assert_incrementing_instruction(
        loader=loader,
        constants=consts,
        instruction=constant_instruction('getstatic', field_ref),
        expected=[
            Push(value)
        ]
    )
