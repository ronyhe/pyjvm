from jawa.constants import ConstantPool

from pyjvm.model.hierarchies import does_type_derive_from, simple_instance_check
from pyjvm.model.jvm_class import JvmClass
from pyjvm.model.jvm_types import ObjectReferenceType, RootObjectType, ArrayReferenceType
from pyjvm.utils.utils import class_as_descriptor
from test.utils import DUMMY_SUB_CLASS_NAME, DUMMY_CLASS, dummy_loader

_DUMMY_DESCRIPTOR = class_as_descriptor(DUMMY_CLASS.name)
_DUMMY_SUB_DESCRIPTOR = class_as_descriptor(DUMMY_SUB_CLASS_NAME)


def instance_test(type_, descriptor, loader=None):
    if loader is None:
        loader = dummy_loader()
    return does_type_derive_from(type_, descriptor, loader)


def test_simple_instance_of():
    assert instance_test(DUMMY_CLASS.type, _DUMMY_DESCRIPTOR)


def test_parent_not_instance_of_child():
    assert not instance_test(DUMMY_CLASS.type, _DUMMY_SUB_DESCRIPTOR)


def test_child_is_instance_of_parent():
    assert instance_test(ObjectReferenceType(DUMMY_SUB_CLASS_NAME), _DUMMY_DESCRIPTOR)


def test_instance_of_interface():
    interface_name = 'Interface'
    implementor_name = 'Implementor'
    root_name = RootObjectType.refers_to

    interface = JvmClass(
        interface_name,
        root_name,
        ConstantPool()
    )

    implementor = JvmClass(
        implementor_name,
        root_name,
        ConstantPool(),
        interfaces=(interface_name,)
    )

    loader = dummy_loader()
    loader.classes[interface_name] = interface
    loader.classes[implementor_name] = implementor

    assert instance_test(ObjectReferenceType(implementor_name), class_as_descriptor(interface_name), loader)


def test_instance_of_array():
    array_of_dummies = ArrayReferenceType(ObjectReferenceType(DUMMY_CLASS.name))
    assert instance_test(array_of_dummies, '[' + _DUMMY_DESCRIPTOR)


def test_instance_of_parent_interface(std_loader):
    # In the java/io package the class FileOutputStream extends OutputStream
    # And OutputStream implement the Closeable interface.
    # So FileOutputStream, the sub class, should be an instance of Closable,
    # the interface implemented by the super class
    assert simple_instance_check('java/io/FileOutputStream', 'java/io/Closeable', std_loader)
