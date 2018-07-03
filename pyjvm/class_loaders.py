from pyjvm.jvm_types import RootObjectType


def _name_and_default_value(pair):
    name, type_ = pair
    return name, type_.create_instance(type_.default_value)


class LoaderEntry:
    def __init__(self, jvm_class, statics):
        self.jvm_class = jvm_class
        self.statics = statics


class ClassLoader:
    def __init__(self):
        self._map = dict()
        self.first_load_function = None

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
        acc.add(class_name)
        curr = class_name
        while not curr == RootObjectType.refers_to:
            the_class = self.get_the_class(curr)
            next_name = the_class.name_of_base
            acc.add(next_name)
            curr = next_name

        return acc


class FixedClassLoader(ClassLoader):
    def __init__(self, classes):
        super().__init__()
        self.classes = dict(classes)

    def _load_jvm_class(self, name):
        return self.classes[name]
