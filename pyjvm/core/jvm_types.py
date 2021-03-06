from typing import Dict


class Type:
    def __init__(self, name, *, default_value, refers_to=None,
                 needs_two_slots=False, is_array_reference=False):
        self.name: str = str(name)
        self.is_reference: bool = refers_to is not None
        self.is_value = not self.is_reference
        self.needs_two_slots: bool = bool(needs_two_slots)
        self.refers_to = refers_to
        self.default_value = default_value
        self.is_class_reference: bool = isinstance(refers_to, str)
        self.is_array_reference: bool = is_array_reference
        self.validate()

    def validate(self):
        if self.default_value is None:
            raise ValueError('Types must have default values')
        if self.is_reference and self.refers_to is None:
            raise ValueError('Reference types must specify a referred type')
        if self.is_array_reference and not self.is_reference:
            raise ValueError('How can an array reference not be a reference?')
        if self.is_class_reference and not self.is_reference:
            raise ValueError('How can a reference to a class not be a reference?')
        if self.is_value and any((self.is_reference, self.is_class_reference, self.is_array_reference)):
            raise ValueError('Types cannot be value types and reference types at the same time')

    def create_instance(self, value):
        return JvmValue(self, value)

    def __repr__(self):
        return f'{self.__class__.__name__}(refers_to={self.refers_to})'

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return isinstance(other, Type) and other.name == self.name

    def __hash__(self):
        return hash(self.name)


class _SimpleNameType(Type):
    def __repr__(self):
        return str(self)


class _FloatingPointType(_SimpleNameType):
    def create_instance(self, value):
        return super().create_instance(float(value))


Integer = _SimpleNameType('<Integer>', default_value=0)
Float = _FloatingPointType('<Float>', default_value=0.0)
Long = _SimpleNameType('<Long>', default_value=0, needs_two_slots=True)
Double = _FloatingPointType('<Double>', default_value=0.0, needs_two_slots=True)


class _NullClass:
    def __repr__(self):
        return '<NULL>'


NULL_OBJECT = _NullClass()


class _ReferenceType(Type):
    def __init__(self, name, refers_to, is_array_reference=False):
        super().__init__(name, refers_to=refers_to, default_value=NULL_OBJECT, is_array_reference=is_array_reference)


class ObjectReferenceType(_ReferenceType):
    def __init__(self, refers_to):
        super().__init__('<Object>', refers_to=refers_to)


class ArrayReferenceType(_ReferenceType):
    def __init__(self, refers_to):
        super().__init__('<Array>', refers_to=refers_to, is_array_reference=True)


class JvmValue:
    def __init__(self, type_, value):
        self.type: Type = type_
        self.value = value
        self.is_null = value == NULL_OBJECT
        if self.is_null and not self.type.is_reference:
            raise TypeError('Only reference types can have NULL values')

    def __eq__(self, other):
        try:
            return self.type == other.type and self.value == other.value
        except AttributeError:
            return False

    def __repr__(self):
        return f'{self.__class__.__name__}({repr(self.type)}, {repr(self.value)})'

    def __str__(self):
        return f'{self.__class__.__name__}({self.type.name}, {repr(self.value)})'

    def duplicate(self):
        return self.__class__(self.type, self.value)


class CompType:
    def __init__(self, type_or_value):
        if not isinstance(type_or_value, Type):
            type_ = type_or_value.type
        else:
            type_ = type_or_value

        self.is_two = type_ in (Long, Double)
        self.is_one = not self.is_two


class JvmObject:
    """The value of a reference class instance at runtime

    To be used in conjunction with a JvmType, as the value for reference types.

    fields: Mapping[name, JvmType], the names and types of the fields in this object's class
    """

    @classmethod
    def defaults(cls, field_specs):
        """Return a new JvmObject with all fields initialized to their default values"""
        return cls(
            (name, type_.create_instance(type_.default_value)) for name, type_ in dict(field_specs).items()
        )

    def __init__(self, fields):
        self.fields: Dict[str, JvmValue] = dict(fields)

    def __eq__(self, other):
        try:
            return other.fields == self.fields
        except AttributeError:
            return False

    def __repr__(self):
        return f'<{self.__class__.__name__}>'


RootObjectType = ObjectReferenceType('java/lang/Object')

NULL_VALUE = RootObjectType.create_instance(NULL_OBJECT)
