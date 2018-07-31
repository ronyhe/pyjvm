from jawa.classloader import ClassLoader as JawaLoader

from pyjvm.core.jvm_types import RootObjectType, ObjectReferenceType, JvmObject
from pyjvm.utils.jawa_conversions import convert_class_file
from pyjvm.utils.utils import path_to_std_lib_as_str


class LoaderEntry:
    """An object that represents a JVM class at runtime

    Attributes
        - jvm_class - A instance of JvmClass
        - statics - A dictionary from names (str) to instances of JvmValue
    """

    def __init__(self, jvm_class, statics):
        self.jvm_class = jvm_class
        self.statics = statics


class ClassLoader:
    """An abstract object that provides access to load entries.

    It operates around a private dictionary object `self._map`, which maps names to `LoadEntry` objects.
    When the get operation is called, it checks whether or not the class is already in the map.
    If it isn't, the loader loads the class and runs the `first_load_function`.
    This ensures that the actual loading operations occur once and only once.

    It's acceptable to assign the `first_load_function` after creating the instance.
    But it's recommended to do so as early as possible and before actual usage, since loading classes before assignment
    will create classes that weren't initialized as expected.

    Subclasses should implement to `_load_jvm_class` which is the only abstract method.
    """

    def __init__(self, first_load_function=None):
        """ Create a `ClassLoader`

        The `first_load_function` will be called the first time a class loaded and the class will be passed to it.
        It will not be called again when the same class is accessed.
        """
        self._map = dict()
        self.first_load_function = first_load_function

    def _load_jvm_class(self, name):
        """Load the class of the given name, usually from a JAR or .class file, and return a `JvmClass` instance

        This method will only be called once for a given name
        """
        raise NotImplementedError()

    def _create_entry(self, name):
        jvm_class = self._load_jvm_class(name)
        statics = dict(_name_and_default_value(pair) for pair in jvm_class.static_fields.items())
        return LoaderEntry(jvm_class, statics)

    def __getitem__(self, item):
        """Return a `ClassEntry` object according to the provided name.

        Performs initial loading and initializing only if needed
        """
        if item not in self._map:
            entry = self._create_entry(item)
            self._map[item] = entry
            if self.first_load_function is not None:
                self.first_load_function(entry.jvm_class)

        return self._map[item]

    def get_the_class(self, name):
        """Get the class instead of the entry, equivalent to loader[name].jvm_class"""
        return self[name].jvm_class

    def get_the_statics(self, name):
        """Get the statics instead of the entry, equivalent to loader[name].statics"""
        return self[name].statics

    def super_classes(self, class_name):
        """Return a list of the names of all the superclasses the class has.

        The list goes from bottom to top.
        Presumably, for any class that is actually found, the resulting list will always:
         - Have size 1 or greater. `len(self.super_classes(name)) > = 1`
         - Start with the class itself.
         - End with java/lang/Object.
        """
        acc = [class_name]
        # noinspection PyUnresolvedReferences
        curr = class_name
        while not curr == RootObjectType.refers_to:
            the_class = self.get_the_class(curr)
            next_name = the_class.name_of_base
            acc.append(next_name)
            curr = next_name

        if len(acc) < 1:
            raise ValueError('super classes are expected to have at least one item')
        if not acc[0] == class_name:
            raise ValueError('super classes are expected to begin with the class that was queried upon')
        if not acc[-1] == RootObjectType.refers_to:
            raise ValueError('super_class are expected to end with the root type java/lang/Object')

        return acc

    def collect_fields_in_super_classes(self, class_name):
        """Return a dictionary of the fields in the class hierarchy

        This means the fields all classes that are returned from `get_ancestors`.
        """
        dic = {}
        for sup in self.super_classes(class_name):
            if not sup == RootObjectType.refers_to:
                class_ = self.get_the_class(sup)
                for name, type_ in class_.fields.items():
                    if name not in dic:
                        dic[name] = type_

        return dic

    def ancestor_set(self, class_name):
        """Return a set of all possible parents as relevant for instance-of relationships

        An instance of class A is an instance-of a class B if and only if the B
        exists in the set of all classes the A derives from.
        We'll call that set the ancestor set and define it recursively. It contains:
         - A
         - The ancestor set for all interfaces that A implements
         - The ancestor set for A's base class, unless A is already the root class (java/lang/Object)
        See hierarchies.py for a complete definition
        """

        def loop(name, the_set):
            the_class = self.get_the_class(name)
            the_set.add(name)
            for interface in the_class.interfaces:
                the_set.update(self.ancestor_set(interface))
            name_of_base = the_class.name_of_base
            if name == RootObjectType.refers_to or name_of_base is None:
                return the_set
            else:
                return loop(name_of_base, the_set)

        return loop(class_name, set())

    def resolve_method(self, class_name, method_key):
        for name in self.super_classes(class_name):
            class_ = self.get_the_class(name)
            try:
                return class_.methods[method_key]
            except KeyError:
                pass

        raise KeyError(f'Cannot resolve method {class_name}#{method_key.name}{method_key.descriptor}')

    def default_instance(self, class_name):
        """Returns an instance of the class with all fields initialized to their type's default value

        See core.jvm_types.py for more information regarding types and their defaults.
        """
        fields = self.collect_fields_in_super_classes(class_name)
        obj = JvmObject.defaults(fields)

        type_ = ObjectReferenceType(class_name)
        instance = type_.create_instance(obj)
        return instance


class FixedClassLoader(ClassLoader):
    """A loader that loads classes from a predefined dictionary. Useful for testing"""

    def __init__(self, classes):
        super().__init__()
        self.classes = dict(classes)

    def _load_jvm_class(self, name):
        return self.classes[name]


class TraditionalLoader(ClassLoader):
    """A loader that loads classes from JAR and .class files according to Java classpath conventions

    Delegates work to jawa.classloader.ClassLoader, refer to that class for more info
    """

    def __init__(self, cp_string):
        super().__init__()
        parts = [cp.strip() for cp in cp_string.split(':')]
        parts = [cp for cp in parts if cp]
        parts.insert(0, path_to_std_lib_as_str())
        self._jawa_loader = JawaLoader(*parts)

    def _load_jvm_class(self, name):
        cf = self._jawa_loader[name]
        class_ = convert_class_file(cf)
        return class_


def _name_and_default_value(pair):
    name, type_ = pair
    return name, type_.create_instance(type_.default_value)
