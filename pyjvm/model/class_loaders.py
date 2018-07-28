from jawa.classloader import ClassLoader as JawaLoader

from pyjvm.model.jvm_class import JvmObject
from pyjvm.model.jvm_types import RootObjectType, ObjectReferenceType
from pyjvm.utils.jawa_conversions import convert_class_file


def _name_and_default_value(pair):
    name, type_ = pair
    return name, type_.create_instance(type_.default_value)


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

    def get_ancestors(self, class_name):
        """Return a set of the names of all the superclasses the class has

        The set includes the `class_name` itself and the root class java/lang/Object
        """
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
        """Return a dictionary of the fields in the class hierarchy

        This means the fields all classes that are returned from `get_ancestors`.
        """
        acc = dict()
        name = class_name
        while not name == RootObjectType.refers_to:
            the_class = self.get_the_class(name)
            acc.update(the_class.fields)
            name = the_class.name_of_base

        return acc

    def default_instance(self, class_name):
        """Returns an instance of the class with all fields initialized to their type's default value

        See model.jvm_types.py for more information regarding types and their defaults.
        """
        fields = self.collect_fields_in_ancestors(class_name)
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
        # noinspection PyUnresolvedReferences
        self._jawa_loader = JawaLoader(*cp_string.split(':'))

    def _load_jvm_class(self, name):
        cf = self._jawa_loader[name]
        class_ = convert_class_file(cf)
        return class_
