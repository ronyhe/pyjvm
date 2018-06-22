from pyjvm.types import Type, RootObjectType


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


class _NullClass:
    def __repr__(self):
        return '<NULL>'


NULL_OBJECT = _NullClass()

NULL_VALUE = JvmValue(RootObjectType, NULL_OBJECT)
