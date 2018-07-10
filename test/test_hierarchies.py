from jawa.constants import ConstantPool

from pyjvm.hierarchies import is_type_instance_of
from pyjvm.jvm_class import JvmClass
from pyjvm.jvm_types import ObjectReferenceType, RootObjectType, ArrayReferenceType
from pyjvm.utils import class_as_descriptor
from test.utils import DUMMY_SUB_CLASS_NAME, DUMMY_CLASS, dummy_loader

_DUMMY_DESCRIPTOR = class_as_descriptor(DUMMY_CLASS.name)
_DUMMY_SUB_DESCRIPTOR = class_as_descriptor(DUMMY_SUB_CLASS_NAME)


def instance_test(type_, descriptor, loader=None):
    if loader is None:
        loader = dummy_loader()
    return is_type_instance_of(type_, descriptor, loader)


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
        names_of_interfaces=(interface_name,)
    )

    loader = dummy_loader()
    loader.classes[interface_name] = interface
    loader.classes[implementor_name] = implementor

    assert instance_test(ObjectReferenceType(implementor_name), class_as_descriptor(interface_name), loader)


def test_instance_of_array():
    array_of_dummies = ArrayReferenceType(ObjectReferenceType(DUMMY_CLASS.name))
    assert instance_test(array_of_dummies, '[' + _DUMMY_DESCRIPTOR)
