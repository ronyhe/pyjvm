from jawa.util.bytecode import Operand, OperandTypes, Instruction

from pyjvm import value_array_type_indicators
from pyjvm.jvm_class import JvmObject
from pyjvm.jvm_types import Integer, ArrayReferenceType, RootObjectType
from pyjvm.utils import class_as_descriptor
from test.old_tests.test_utils import BlankTestMachine, DUMMY_SUB_CLASS_NAME, DUMMY_CLASS, dummy_loader

_SOME_INT = Integer.create_instance(54)


class RefTestMachine(BlankTestMachine):
    def __init__(self):
        super().__init__()
        self.class_loader = dummy_loader()

    def step_constant(self, name, constant):
        instruction = Instruction.create(name, [Operand(OperandTypes.CONSTANT_INDEX, constant.index)])
        self.step_instruction(instruction)


def test_get_static():
    machine = RefTestMachine()
    field_ref = DUMMY_CLASS.class_field_ref(machine.current_constants())
    value = Integer.create_instance(4)

    machine.class_loader[DUMMY_CLASS.name].statics[DUMMY_CLASS.class_field.name] = value
    machine.step_constant('getstatic', field_ref)
    assert machine.current_op_stack().peek() == value


def test_set_static():
    machine = RefTestMachine()
    field_ref = DUMMY_CLASS.class_field_ref(machine.current_constants())
    value = Integer.create_instance(10)
    machine.current_op_stack().push(value)
    machine.step_constant('putstatic', field_ref)
    assert machine.current_op_stack().size() == 0
    assert machine.class_loader[DUMMY_CLASS.name].statics[DUMMY_CLASS.class_field.name] == value


def test_new():
    machine = RefTestMachine()
    class_ref = machine.current_constants().create_class(DUMMY_CLASS.name)
    machine.step_constant('new', class_ref)
    tos = machine.current_op_stack().peek()
    assert tos.type == DUMMY_CLASS.type
    assert isinstance(tos.value, JvmObject)


def test_new_inits_fields_to_defaults():
    machine = RefTestMachine()
    class_ref = machine.current_constants().create_class(DUMMY_CLASS.name)
    machine.step_constant('new', class_ref)

    actual = machine.current_op_stack().peek()
    assert actual.type == DUMMY_CLASS.type
    assert actual.value.fields[DUMMY_CLASS.instance_field.name.value] == Integer.create_instance(Integer.default_value)


def test_new_inits_super_field_to_defaults():
    machine = RefTestMachine()
    class_ref = machine.current_constants().create_class(DUMMY_SUB_CLASS_NAME)
    machine.step_constant('new', class_ref)
    tos = machine.current_op_stack().peek()
    assert tos.value.fields[DUMMY_CLASS.instance_field.name.value] == Integer.create_instance(Integer.default_value)


def test_put_field():
    machine = RefTestMachine()
    stack = machine.current_op_stack()

    field_ref = DUMMY_CLASS.instance_field_ref(machine.current_constants())
    instance = machine.create_new_class_instance(DUMMY_CLASS.name)
    value = Integer.create_instance(15)

    stack.push(instance)
    stack.push(value)

    machine.step_constant('putfield', field_ref)
    assert instance.value.fields[DUMMY_CLASS.instance_field.name] == value


def test_get_field():
    machine = RefTestMachine()
    field_ref = DUMMY_CLASS.instance_field_ref(machine.current_constants())
    instance = machine.create_new_class_instance(DUMMY_CLASS.name)
    instance.value.fields[DUMMY_CLASS.instance_field.name] = _SOME_INT
    stack = machine.current_op_stack()
    stack.push(instance)
    machine.step_constant('getfield', field_ref)
    assert stack.size() == 1
    assert stack.peek() == _SOME_INT


def test_new_array():
    machine = BlankTestMachine()
    stack = machine.current_op_stack()
    stack.push(_SOME_INT)
    type_indicator = value_array_type_indicators.indicator_by_type(Integer)
    machine.step_instruction('newarray', [Operand(OperandTypes.LITERAL, type_indicator)])
    assert stack.size() == 1
    integers = [Integer.create_instance(Integer.default_value) for _ in range(_SOME_INT.value)]
    type_ = ArrayReferenceType(Integer)
    expected_value = type_.create_instance(integers)
    actual = stack.peek()
    assert actual == expected_value


def test_new_ref_array():
    machine = RefTestMachine()
    class_constant = machine.current_constants().create_class(DUMMY_CLASS.name)
    stack = machine.current_op_stack()
    stack.push(_SOME_INT)
    machine.step_constant('anewarray', class_constant)
    tos = stack.peek()
    type_ = DUMMY_CLASS.type
    assert tos.type == ArrayReferenceType(type_)
    assert tos.value == [type_.create_instance(type_.default_value) for _ in range(_SOME_INT.value)]


def test_array_length():
    machine = BlankTestMachine()
    length = 43
    array = ArrayReferenceType(RootObjectType).create_instance([None] * length)
    stack = machine.current_op_stack()
    stack.push(array)
    machine.step_instruction('arraylength')
    assert stack.peek() == Integer.create_instance(length)


def test_instance_of():
    machine = RefTestMachine()
    descriptor = class_as_descriptor(DUMMY_CLASS.name)
    descriptor_constant = machine.current_constants().create_utf8(descriptor)

    instance = DUMMY_CLASS.type.create_instance(JvmObject(dict()))
    stack = machine.current_op_stack()
    stack.push(instance)

    machine.step_constant('instanceof', descriptor_constant)
    assert stack.size() == 1
    assert stack.peek() == Integer.create_instance(1)
