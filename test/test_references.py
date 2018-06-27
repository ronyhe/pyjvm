from jawa.cf import ClassFile
from jawa.util.bytecode import Operand, OperandTypes

from pyjvm.class_loaders import FixedClassLoader
from pyjvm.jawa_conversions import convert_class_file
from pyjvm.jvm_class import JvmObject
from pyjvm.jvm_types import Integer, ObjectReferenceType
from test.test_utils import BlankTestMachine


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


_DUMMY = _DummyClass()
_LOADER = FixedClassLoader({_DUMMY.name: convert_class_file(_DUMMY.class_file)})


def _machine():
    m = BlankTestMachine()
    m.class_loader = _LOADER
    return m


def test_get_static():
    machine = _machine()
    field_ref = _DUMMY.class_field_ref(machine.current_constants())
    machine.load_class(_DUMMY.name)
    value = Integer.create_instance(4)

    machine.statics[_DUMMY.name][_DUMMY.class_field.name] = value
    machine.step_instruction('getstatic', [Operand(OperandTypes.CONSTANT_INDEX, field_ref.index)])
    assert machine.current_op_stack().peek() == value


def test_new():
    machine = _machine()
    class_ref = machine.current_constants().create_class(_DUMMY.name)
    machine.step_instruction('new', [Operand(OperandTypes.CONSTANT_INDEX, class_ref.index)])
    tos = machine.current_op_stack().peek()
    assert tos.type == _DUMMY.type
    assert isinstance(tos.value, JvmObject)


def test_new_inits_fields_to_defaults():
    machine = _machine()
    class_ref = machine.current_constants().create_class(_DUMMY.name)
    machine.step_instruction('new', [Operand(OperandTypes.CONSTANT_INDEX, class_ref.index)])

    actual = machine.current_op_stack().peek()
    assert actual.type == _DUMMY.type
    assert actual.value.fields[_DUMMY.instance_field.name.value] == Integer.create_instance(Integer.default_value)


def test_new_inits_super_field_to_defaults():
    pass
