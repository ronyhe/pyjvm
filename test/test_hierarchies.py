from pyjvm.hierarchies import is_type_instance_of
from pyjvm.jvm_types import ObjectReferenceType
from test.test_utils import dummy_loader, DUMMY_CLASS, DUMMY_SUB_CLASS_NAME


def instance_test(type_, descriptor):
    return is_type_instance_of(type_, descriptor, dummy_loader())


def test_simple_instance_of():
    assert instance_test(DUMMY_CLASS.type, 'L' + DUMMY_CLASS.name + ';')


def test_parent_not_instance_of_child():
    assert not instance_test(DUMMY_CLASS.type, 'L' + DUMMY_SUB_CLASS_NAME + ';')


def test_child_is_instance_of_parent():
    assert instance_test(ObjectReferenceType(DUMMY_SUB_CLASS_NAME), 'L' + DUMMY_CLASS.name + ';')


def test_instance_of_interface():
    pass


def test_instance_of_array():
    pass
