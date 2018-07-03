from jawa.util.descriptor import field_descriptor

from pyjvm.class_loaders import ClassLoader
from pyjvm.jawa_conversions import convert_type
from pyjvm.jvm_types import JvmValue, Type


def is_value_instance_of(instance: JvmValue, descriptor_for_possible_parent: str, loader: ClassLoader) -> bool:
    if instance.is_null:
        raise ValueError('Cannot instance_of check null value')

    return is_type_instance_of(instance.type, descriptor_for_possible_parent, loader)


def is_type_instance_of(instance_type: Type, descriptor_for_possible_parent: str, loader: ClassLoader) -> bool:
    if instance_type.is_value:
        raise ValueError('Cannot instance_of check value types. Only references')

    descriptor_type = convert_type(field_descriptor(descriptor_for_possible_parent))
    if instance_type.is_array_reference and descriptor_type.is_array_reference:
        return _is_array_instance_of_array(instance_type, descriptor_type, loader)
    elif instance_type.is_class_reference and descriptor_type.is_class_reference:
        return _is_class_instance_of_class(instance_type, descriptor_type, loader)
    else:
        return False


def _is_array_instance_of_array(instance_type, descriptor_type, loader):
    raise NotImplementedError()


def _is_class_instance_of_class(instance_type, descriptor_type, loader):
    instance_class_name = instance_type.refers_to
    instance_interfaces = loader.get_the_class(instance_class_name).interfaces
    possible_roots = list(instance_interfaces) + [instance_class_name]
    return any(descriptor_type.refers_to in loader.get_ancestors(root) for root in possible_roots)
