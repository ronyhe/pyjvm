from jawa.cf import ClassFile
from jawa.util.bytecode import Operand, OperandTypes, Instruction

from pyjvm import value_array_type_indicators
from pyjvm.class_loaders import FixedClassLoader
from pyjvm.jawa_conversions import convert_class_file
from pyjvm.jvm_class import JvmObject
from pyjvm.jvm_types import Integer, ObjectReferenceType, ArrayReferenceType, RootObjectType
from test.test_utils import BlankTestMachine

_SOME_INT = Integer.create_instance(54)


class _DummyClass:
    DESCRIPTOR = 'I'

    def __init__(self):
        self.name = 'ClassName'
        self.class_file = ClassFile.create(self.name)
        self.instance_field = self.class_file.fields.create('instance_field', self.DESCRIPTOR)
        self.class_field = self.class_file.fields.create('class_field', self.DESCRIPTOR)
        self.class_field.access_flags.set('acc_static', True)
        self.type = ObjectReferenceType(self.name)

    def create_field_ref(self, constants, field):
        return constants.create_field_ref(self.name, field.name, self.DESCRIPTOR)

    def instance_field_ref(self, constants):
        return self.create_field_ref(constants, self.instance_field)

    def class_field_ref(self, constants):
        return self.create_field_ref(constants, self.class_field)


_SUB_CLASS_NAME = 'Sub'
_DUMMY = _DummyClass()

_LOADER = FixedClassLoader({
    _DUMMY.name: convert_class_file(_DUMMY.class_file),
    _SUB_CLASS_NAME: convert_class_file(ClassFile.create(_SUB_CLASS_NAME, _DUMMY.name))
})


class RefTestMachine(BlankTestMachine):
    def __init__(self):
        super().__init__()
        self.class_loader = _LOADER

    def step_constant(self, name, constant):
        instruction = Instruction.create(name, [Operand(OperandTypes.CONSTANT_INDEX, constant.index)])
        self.step_instruction(instruction)


def test_get_static():
    machine = RefTestMachine()
    field_ref = _DUMMY.class_field_ref(machine.current_constants())
    machine.load_class(_DUMMY.name)
    value = Integer.create_instance(4)

    machine.statics[_DUMMY.name][_DUMMY.class_field.name] = value
    machine.step_constant('getstatic', field_ref)
    assert machine.current_op_stack().peek() == value


def test_set_static():
    machine = RefTestMachine()
    field_ref = _DUMMY.class_field_ref(machine.current_constants())
    machine.load_class(_DUMMY.name)
    value = Integer.create_instance(10)
    machine.current_op_stack().push(value)
    machine.step_constant('putstatic', field_ref)
    assert machine.current_op_stack().size() == 0
    assert machine.statics[_DUMMY.name][_DUMMY.class_field.name] == value


def test_new():
    machine = RefTestMachine()
    class_ref = machine.current_constants().create_class(_DUMMY.name)
    machine.step_constant('new', class_ref)
    tos = machine.current_op_stack().peek()
    assert tos.type == _DUMMY.type
    assert isinstance(tos.value, JvmObject)


def test_new_inits_fields_to_defaults():
    machine = RefTestMachine()
    class_ref = machine.current_constants().create_class(_DUMMY.name)
    machine.step_constant('new', class_ref)

    actual = machine.current_op_stack().peek()
    assert actual.type == _DUMMY.type
    assert actual.value.fields[_DUMMY.instance_field.name.value] == Integer.create_instance(Integer.default_value)


def test_new_inits_super_field_to_defaults():
    machine = RefTestMachine()
    class_ref = machine.current_constants().create_class(_SUB_CLASS_NAME)
    machine.step_constant('new', class_ref)
    tos = machine.current_op_stack().peek()
    assert tos.value.fields[_DUMMY.instance_field.name.value] == Integer.create_instance(Integer.default_value)


def test_put_field():
    machine = RefTestMachine()
    stack = machine.current_op_stack()

    field_ref = _DUMMY.instance_field_ref(machine.current_constants())
    instance = machine.create_new_class_instance(_DUMMY.name)
    value = Integer.create_instance(15)

    stack.push(instance)
    stack.push(value)

    machine.step_constant('putfield', field_ref)
    assert instance.value.fields[_DUMMY.instance_field.name] == value


def test_get_field():
    machine = RefTestMachine()
    field_ref = _DUMMY.instance_field_ref(machine.current_constants())
    instance = machine.create_new_class_instance(_DUMMY.name)
    instance.value.fields[_DUMMY.instance_field.name] = _SOME_INT
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
    class_constant = machine.current_constants().create_class(_DUMMY.name)
    stack = machine.current_op_stack()
    stack.push(_SOME_INT)
    machine.step_constant('anewarray', class_constant)
    tos = stack.peek()
    type_ = _DUMMY.type
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


def instance_test(type_, descriptor):
    machine = RefTestMachine()
    return machine.is_reference_an_instance_of(
        type_.create_instance(JvmObject(dict())),
        descriptor
    )


def test_simple_instance_of():
    assert instance_test(_DUMMY.type, 'L' + _DUMMY.name + ';')


def test_parent_not_instance_of_child():
    assert not instance_test(_DUMMY.type, 'L' + _SUB_CLASS_NAME + ';')


def test_child_is_instance_of_parent():
    assert instance_test(ObjectReferenceType(_SUB_CLASS_NAME), 'L' + _DUMMY.name + ';')


def test_instance_of_interface():
    pass


def test_instance_of_array():
    pass
