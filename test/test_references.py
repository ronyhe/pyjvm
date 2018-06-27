from jawa.cf import ClassFile
from jawa.util.bytecode import Operand, OperandTypes

from pyjvm.class_loaders import FixedClassLoader
from pyjvm.jawa_conversions import convert_class_file
from pyjvm.jvm_class import JvmObject
from pyjvm.jvm_types import Integer, ObjectReferenceType
from test.test_utils import BlankTestMachine


def test_get_static():
    class_name = 'ClassName'
    field_name = 'fieldName'
    descriptor = 'I'

    the_class = ClassFile.create(class_name)
    field = the_class.fields.create(field_name, descriptor)
    field.access_flags.set('acc_static', True)
    machine = BlankTestMachine()
    field_ref = machine.current_constants().create_field_ref(class_name, field_name, descriptor)
    machine.class_loader = FixedClassLoader({class_name: convert_class_file(the_class)})
    machine.load_class(class_name)
    value = Integer.create_instance(4)
    machine.statics[class_name][field_name] = value
    machine.step_instruction('getstatic', [Operand(OperandTypes.CONSTANT_INDEX, field_ref.index)])
    assert machine.current_op_stack().peek() == value


def test_new():
    class_name = 'ClassName'
    the_class = ClassFile.create(class_name)
    machine = BlankTestMachine()
    class_ref = machine.current_constants().create_class(class_name)
    machine.class_loader = FixedClassLoader({class_name: convert_class_file(the_class)})
    machine.step_instruction('new', [Operand(OperandTypes.CONSTANT_INDEX, class_ref.index)])
    assert machine.current_op_stack().peek() == ObjectReferenceType(class_name).create_instance(JvmObject(dict()))


def test_new_inits_fields_to_defaults():
    pass


def test_new_inits_super_field_to_defaults():
    pass
