from jawa.util.descriptor import field_descriptor

from pyjvm.model.class_loaders import ClassLoader
from pyjvm.model.jvm_types import JvmValue, Type
from pyjvm.utils.jawa_conversions import convert_type


def is_value_instance_of(instance: JvmValue, descriptor_for_possible_parent: str, loader: ClassLoader) -> bool:
    if instance.is_null:
        raise ValueError('Cannot instance_of check null value')

    return is_type_instance_of(instance.type, descriptor_for_possible_parent, loader)


def is_type_instance_of(instance_type: Type, descriptor_for_possible_parent: str, loader: ClassLoader) -> bool:
    if instance_type.is_value:
        raise ValueError('Cannot instance_of check value types. Only references')

    descriptor_type = convert_type(field_descriptor(descriptor_for_possible_parent))
    return _Checker(loader).is_instance_of(instance_type, descriptor_type)


class _Checker:
    def __init__(self, loader):
        self.loader = loader

    def is_instance_of(self, instance_type, possible_parent_type):
        if instance_type.is_array_reference and possible_parent_type.is_array_reference:
            return self.is_instance_of(instance_type.refers_to, possible_parent_type.refers_to)
        elif instance_type.is_class_reference and possible_parent_type.is_class_reference:
            return self._is_class_instance_of_class(instance_type, possible_parent_type)
        else:
            return False

    def _is_class_instance_of_class(self, instance_type, possible_parent_type):
        instance_class_name = instance_type.refers_to
        instance_class = self.loader.get_the_class(instance_class_name)
        instance_interfaces = instance_class.interfaces
        possible_roots = list(instance_interfaces) + [instance_class_name]
        return any(possible_parent_type.refers_to in self.loader.get_ancestors(root) for root in possible_roots)
