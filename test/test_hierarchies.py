"""Test the functionality of relationship queries in hierarchies.py

These tests rely heavily on the relationship of three classes in the java/io package:
`FileOutputStream` derives from `OutputStream` which implements `Closeable`
"""
from pyjvm.model.hierarchies import does_type_derive_from, simple_instance_check
from pyjvm.model.jvm_types import ObjectReferenceType, ArrayReferenceType
from pyjvm.utils.utils import class_as_descriptor

_IO = 'java/io/'
OUTPUT_STREAM = _IO + 'OutputStream'
FILE_OUTPUT_STREAM = _IO + 'FileOutputStream'
CLOSEABLE = _IO + 'Closeable'


def test_instance_of_class(std_loader):
    assert does_type_derive_from(
        ObjectReferenceType(FILE_OUTPUT_STREAM),
        class_as_descriptor(FILE_OUTPUT_STREAM),
        std_loader
    )


def test_parent_not_instance_of_child(std_loader):
    assert not simple_instance_check(OUTPUT_STREAM, FILE_OUTPUT_STREAM, std_loader)


def test_child_is_instance_of_parent(std_loader):
    assert simple_instance_check(FILE_OUTPUT_STREAM, OUTPUT_STREAM, std_loader)


def test_instance_of_interface(std_loader):
    assert simple_instance_check(OUTPUT_STREAM, CLOSEABLE, std_loader)


def test_instance_of_array(std_loader):
    base_type = ObjectReferenceType(OUTPUT_STREAM)
    array_type = ArrayReferenceType(base_type)

    descriptor = _add_dimensions_to_descriptor(
        class_as_descriptor(OUTPUT_STREAM)
    )

    assert does_type_derive_from(
        array_type,
        descriptor,
        std_loader
    )


def test_instance_of_parent_interface(std_loader):
    assert simple_instance_check(FILE_OUTPUT_STREAM, CLOSEABLE, std_loader)


def _add_dimensions_to_descriptor(descriptor, dimensions=1):
    return '[' * dimensions + descriptor
