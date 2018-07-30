from jawa.constants import ConstantPool
from jawa.util.bytecode import Instruction

from pyjvm.actions import Push, ThrowObject, PushNewInstance, PutField, PutStatic, throw_null_pointer, Pop, \
    throw_negative_array_size, throw_check_cast
from pyjvm.core.class_loaders import FixedClassLoader
from pyjvm.core.jvm_class import JvmObject, JvmClass
from pyjvm.core.jvm_types import Integer, NULL_VALUE, ArrayReferenceType, NULL_OBJECT, ObjectReferenceType, \
    RootObjectType
from pyjvm.instructions.references import create_levels
from pyjvm.utils import value_array_type_indicators
from pyjvm.utils.utils import TRUE, FALSE, constant_operand, literal_operand
from test.utils import assert_incrementing_instruction, assert_instruction, constant_instruction, \
    literal_instruction, NPE_CLASS_NAME, CHECK_CAST_CLASS_NAME


def test_instance_of(std_loader):
    obj = std_loader.default_instance(NPE_CLASS_NAME)
    consts = ConstantPool()
    const = consts.create_class(NPE_CLASS_NAME)
    instruction = constant_instruction('instanceof', const)

    assert_incrementing_instruction(
        instruction=instruction,
        constants=consts,
        loader=std_loader,
        op_stack=[obj],
        expected=[
            Push(TRUE)
        ]
    )


def test_not_instance_of(std_loader):
    consts = ConstantPool()
    const = consts.create_class(NPE_CLASS_NAME)
    instruction = constant_instruction('instanceof', const)

    assert_incrementing_instruction(
        instruction=instruction,
        constants=consts,
        loader=std_loader,
        op_stack=[NULL_VALUE],
        expected=[
            Pop(),
            Push(FALSE)
        ]
    )


def test_check_cast(std_loader):
    class_name = NPE_CLASS_NAME
    obj = std_loader.default_instance(NPE_CLASS_NAME)

    consts = ConstantPool()
    const = consts.create_class(class_name)

    assert_incrementing_instruction(
        constants=consts,
        instruction=constant_instruction('checkcast', const),
        op_stack=[obj],
        expected=[],
        loader=std_loader
    )


def test_check_null_cast():
    consts = ConstantPool()
    const = consts.create_class(NPE_CLASS_NAME)

    assert_incrementing_instruction(
        constants=consts,
        instruction=constant_instruction('checkcast', const),
        op_stack=[NULL_VALUE],
        expected=[]
    )


def test_negative_check_cast(std_loader):
    # Obviously, NullPointerException is not an instance of CheckCastException
    consts = ConstantPool()
    const = consts.create_class(CHECK_CAST_CLASS_NAME)
    obj = std_loader.default_instance(NPE_CLASS_NAME)

    assert_instruction(
        constants=consts,
        instruction=constant_instruction('checkcast', const),
        op_stack=[obj],
        expected=[throw_check_cast()],
        loader=std_loader
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
            throw_null_pointer()
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
    class_name = NPE_CLASS_NAME
    type_ = ObjectReferenceType(class_name)

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


def test_multi_new_array():
    class_name = NPE_CLASS_NAME
    type_ = ObjectReferenceType(NPE_CLASS_NAME)

    consts = ConstantPool()
    const = consts.create_class(class_name)

    array_type = ArrayReferenceType(
        ArrayReferenceType(
            type_
        )
    )

    sizes = 2, 3
    null = type_.create_instance(NULL_OBJECT)
    expected_value = array_type.create_instance([
        [null] * 3,
        [null] * 3
    ])

    instruction = Instruction.create('multianewarray', [
        constant_operand(const),
        literal_operand(len(sizes))
    ])
    assert_incrementing_instruction(
        constants=consts,
        instruction=instruction,
        op_stack=[Integer.create_instance(v) for v in sizes],
        expected=[
            Pop(2),
            Push(expected_value)
        ]
    )


def test_levels():
    assert create_levels([2, 3], lambda: 1) == [
        [1, 1, 1],
        [1, 1, 1]
    ]


def test_negative_array_size():
    type_ = Integer
    indicator = value_array_type_indicators.indicator_by_type(type_)
    assert_instruction(
        instruction=literal_instruction('newarray', indicator),
        op_stack=[Integer.create_instance(-4)],
        expected=[
            throw_negative_array_size()
        ]
    )


def test_a_throw():
    type_ = ObjectReferenceType(NPE_CLASS_NAME)
    obj = type_.create_instance(JvmObject(dict()))

    assert_instruction(
        instruction='athrow',
        op_stack=[obj],
        expected=[
            ThrowObject(obj)
        ]
    )


def test_new(std_loader):
    consts = ConstantPool()
    const = consts.create_class(NPE_CLASS_NAME)
    class_ = std_loader.get_the_class(NPE_CLASS_NAME)

    assert_incrementing_instruction(
        constants=consts,
        instruction=constant_instruction('new', const),
        expected=[
            PushNewInstance(class_)
        ],
        loader=std_loader
    )


def test_get_field():
    consts = ConstantPool()
    field_name = 'some_name'
    field_ref = consts.create_field_ref(NPE_CLASS_NAME, field_name, 'I')

    value = Integer.create_instance(50)
    fields = {
        field_name: value
    }
    obj = ObjectReferenceType(NPE_CLASS_NAME).create_instance(JvmObject(fields))

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
    field_name = 'some_field'
    consts = ConstantPool()
    field_ref = consts.create_field_ref(NPE_CLASS_NAME, field_name, 'I')

    value = Integer.create_instance(50)
    fields = {
        field_name: Integer.create_instance(Integer.default_value)
    }
    obj = ObjectReferenceType(NPE_CLASS_NAME).create_instance(JvmObject(fields))

    assert_incrementing_instruction(
        instruction=constant_instruction('putfield', field_ref),
        constants=consts,
        op_stack=[value, obj],
        expected=[
            Pop(2),
            PutField(obj, field_name, value)
        ]
    )


def test_put_static():
    field_name = 'some_name'

    consts = ConstantPool()
    field_ref = consts.create_field_ref(NPE_CLASS_NAME, field_name, 'I')

    value = Integer.create_instance(45)

    assert_incrementing_instruction(
        constants=consts,
        instruction=constant_instruction('putstatic', field_ref),
        op_stack=[value],
        expected=[
            Pop(),
            PutStatic(NPE_CLASS_NAME, field_name, value)
        ]
    )


def test_get_static():
    field_name = 'some_name'

    consts = ConstantPool()
    field_ref = consts.create_field_ref(NPE_CLASS_NAME, field_name, 'I')

    value = Integer.create_instance(67)
    loader = FixedClassLoader({
        NPE_CLASS_NAME: JvmClass(NPE_CLASS_NAME, RootObjectType.refers_to, consts, static_fields={
            field_name: Integer
        })
    })

    loader.get_the_statics(NPE_CLASS_NAME)[field_name] = value

    assert_incrementing_instruction(
        loader=loader,
        constants=consts,
        instruction=constant_instruction('getstatic', field_ref),
        expected=[
            Push(value)
        ]
    )
