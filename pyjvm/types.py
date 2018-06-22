from pyjvm.values import NULL_OBJECT


class Type:
    def __init__(self, name, *, default_value, refers_to=None, needs_two_slots=False, is_array_reference=False):
        self.name: str = str(name)
        self.is_reference: bool = refers_to is not None
        self.is_value = not self.is_reference
        self.needs_two_slots: bool = bool(needs_two_slots)
        self.referenced_type = refers_to
        self.default_value = default_value
        self.is_reference_to_class: bool = isinstance(refers_to, str)
        self.is_array_reference: bool = is_array_reference
        self.validate()

    def validate(self):
        if self.default_value is None:
            raise ValueError('Types must have default values')
        if self.is_reference and self.referenced_type is None:
            raise ValueError('Reference types must specify a referred type')
        if self.is_array_reference and not self.is_reference:
            raise ValueError('How can an array reference not be a reference?')
        if self.is_reference_to_class and not self.is_reference:
            raise ValueError('How can a reference to a class not be a reference?')
        if self.is_value and any((self.is_reference, self.is_reference_to_class, self.is_array_reference)):
            raise ValueError('Types cannot be value types and reference types at the same time')

    def __repr__(self):
        fields = 'default_value', 'refers_to', 'needs_two_slots'
        mapping = [(name, getattr(self, name)) for name in fields]
        values_text = ', '.join(f'{name}={value}' for name, value in mapping)
        return f'{self.__class__.__name__}({self.name}, {values_text})'

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return isinstance(other, Type) and other.name == self.name


Integer = Type('<Integer>', default_value=0)
Float = Type('<Float>', default_value=0.0)
Long = Type('<Long>', default_value=0, needs_two_slots=True)
Double = Type('<Double>', default_value=0.0, needs_two_slots=True)


class ObjectReferenceType(_ReferenceType):
    def __init__(self, refers_to):
        super().__init__('<Object>', refers_to=refers_to)


RootObjectType = ObjectReferenceType('java/lang/Object')


class _ReferenceType(Type):
    def __init__(self, name, refers_to, is_array_reference=False):
        super().__init__(name, refers_to=refers_to, default_value=NULL_OBJECT, is_array_reference=is_array_reference)


class ArrayReferenceType(_ReferenceType):
    def __init__(self, refers_to):
        super().__init__('<Array>', refers_to=refers_to, is_array_reference=True)
