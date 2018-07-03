from pyjvm.jvm_class import JvmObject
from pyjvm.jvm_types import ObjectReferenceType
from test.test_utils import BlankTestMachine, dummy_loader, DUMMY_CLASS, DUMMY_SUB_CLASS_NAME


def instance_test(type_, descriptor):
    machine = BlankTestMachine(dummy_loader())
    return machine.is_reference_an_instance_of(
        type_.create_instance(JvmObject(dict())),
        descriptor
    )


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
