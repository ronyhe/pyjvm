import jawa

from pyjvm.model.jvm_class import JvmObject
from pyjvm.model.jvm_types import RootObjectType, ObjectReferenceType
from pyjvm.utils.jawa_conversions import convert_class_file


def _name_and_default_value(pair):
    name, type_ = pair
    return name, type_.create_instance(type_.default_value)


class LoaderEntry:
    def __init__(self, jvm_class, statics):
        self.jvm_class = jvm_class
        self.statics = statics


class ClassLoader:
    def __init__(self, first_load_function=None):
        self._map = dict()
        self.first_load_function = first_load_function

    def _load_jvm_class(self, name):
        raise NotImplementedError()

    def _create_entry(self, name):
        jvm_class = self._load_jvm_class(name)
        statics = dict(_name_and_default_value(pair) for pair in jvm_class.static_fields.items())
        return LoaderEntry(jvm_class, statics)

    def __getitem__(self, item):
        if item not in self._map:
            entry = self._create_entry(item)
            self._map[item] = entry
            if self.first_load_function is not None:
                self.first_load_function(entry.jvm_class)

        return self._map[item]

    def get_the_class(self, name):
        return self[name].jvm_class

    def get_the_statics(self, name):
        return self[name].statics

    def get_ancestors(self, class_name):
        acc = set()
        # noinspection PyUnresolvedReferences
        acc.add(class_name)
        curr = class_name
        while not curr == RootObjectType.refers_to:
            the_class = self.get_the_class(curr)
            next_name = the_class.name_of_base
            acc.add(next_name)
            curr = next_name

        return acc

    def collect_fields_in_ancestors(self, class_name):
        acc = dict()
        name = class_name
        while not name == RootObjectType.refers_to:
            the_class = self.get_the_class(name)
            acc.update(the_class.fields)
            name = the_class.name_of_base

        return acc

    def default_instance(self, class_name):
        fields = self.collect_fields_in_ancestors(class_name)
        obj = JvmObject.defaults(fields)

        type_ = ObjectReferenceType(class_name)
        instance = type_.create_instance(obj)
        return instance


class FixedClassLoader(ClassLoader):
    def __init__(self, classes):
        super().__init__()
        self.classes = dict(classes)

    def _load_jvm_class(self, name):
        return self.classes[name]


class EmptyClassLoader(FixedClassLoader):
    def __init__(self):
        super().__init__(dict())


class TraditionalLoader(ClassLoader):
    def __init__(self, cp_string):
        super().__init__()
        # noinspection PyUnresolvedReferences
        self._jawa_loader = jawa.classloader.ClassLoader(*cp_string.split(':'))

    def _load_jvm_class(self, name):
        cf = self._jawa_loader[name]
        class_ = convert_class_file(cf)
        return class_
