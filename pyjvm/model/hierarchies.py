"""Functions for establishing instance-of relationships

"""
from jawa.util.descriptor import field_descriptor

from pyjvm.model.class_loaders import ClassLoader
from pyjvm.model.jvm_types import JvmValue, Type, ObjectReferenceType
from pyjvm.utils.jawa_conversions import convert_type


def is_value_instance_of(instance: JvmValue, descriptor: str, loader: ClassLoader) -> bool:
    """Return a bool representing whether `instance` is an instance of the class represented by `descriptor`"""
    if instance.is_null:
        raise ValueError('Cannot instance_of check null value')

    return does_type_derive_from(instance.type, descriptor, loader)


def does_type_derive_from(instance_type: Type, descriptor_for_possible_parent: str, loader: ClassLoader) -> bool:
    """Return a bool representing whether `instance_type` derives from the class represented by `descriptor`"""
    if instance_type.is_value:
        raise ValueError('Cannot instance_of check value types. Only references')

    descriptor_type = convert_type(field_descriptor(descriptor_for_possible_parent))
    return _Checker(loader).is_instance_of(instance_type, descriptor_type)


def simple_instance_check(class_name: str, parent_name: str, loader: ClassLoader) -> bool:
    """Return true if instance of the class named `class_name` are instances of the class named `parent_name`"""
    return _Checker(loader).is_instance_of(
        ObjectReferenceType(class_name),
        ObjectReferenceType(parent_name)
    )


class _Checker:
    def __init__(self, loader):
        self.loader = loader

    def is_instance_of(self, instance_type, possible_parent_type):
        if instance_type.is_array_reference and possible_parent_type.is_array_reference:
            # For arrays, perform the query on their underlying types
            return self.is_instance_of(instance_type.refers_to, possible_parent_type.refers_to)
        elif instance_type.is_class_reference and possible_parent_type.is_class_reference:
            return self._does_type_derive_from(instance_type, possible_parent_type)
        else:
            return False

    def _does_type_derive_from(self, instance_type, possible_parent_type):
        """Return True if `possible_parent_type` is in the ancestor set of `instance_typ`

        See class_loaders.py for a complete definition of the ancestor set.
        """
        return possible_parent_type.refers_to in self.loader.ancestor_set(instance_type.refers_to)
