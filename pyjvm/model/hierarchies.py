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
        # `instance_type` is an instance of `possible_parent_type` if and only if
        # possible parent type exists in the set of all the types `instance_type` derives from.
        # That set includes:
        # This class
        # The interfaces this class implements, and their super interfaces
        # The set for this class' super class
        instance_class_name = instance_type.refers_to
        instance_class = self.loader.get_the_class(instance_class_name)
        instance_interfaces = instance_class.interfaces
        possible_roots = list(instance_interfaces) + [instance_class_name]
        return any(possible_parent_type.refers_to in self.loader.get_ancestors(root) for root in possible_roots)
