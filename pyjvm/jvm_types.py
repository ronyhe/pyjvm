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
        fields = 'default_value', 'refers_to', 'needs_two_slots', 'is_type_two_computational_type'
        mapping = [(name, getattr(self, name)) for name in fields]
        values_text = ', '.join(f'{name}={value}' for name, value in mapping)
        return f'{self.__class__.__name__}({self.name}, {values_text})'

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return isinstance(other, Type) and other.name == self.name


class _FloatingPointType(Type):
    def create_instance(self, value):
        return super().create_instance(float(value))


Integer = Type('<Integer>', default_value=0)
Float = _FloatingPointType('<Float>', default_value=0.0)
Long = Type('<Long>', default_value=0, needs_two_slots=True)
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

    def duplicate(self):
        return self.__class__(self.type, self.value)


class CompType:
    def __init__(self, type_or_value):
        if not isinstance(type_or_value, Type):
            type_ = type_or_value.type
        else:
            type_ = type_or_value

        if not type_.is_value:
            raise TypeError(f'Only value types can be computational. The supplied type was {type_}')
        self.is_two = type_ in (Long, Double)
        self.is_one = not self.is_two


RootObjectType = ObjectReferenceType('java/lang/Object')
NULL_VALUE = RootObjectType.create_instance(NULL_OBJECT)
