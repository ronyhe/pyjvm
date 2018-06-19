import enum
from typing import Any, Mapping

import attr
from jawa.cf import ClassFile
from jawa.util.descriptor import JVMType

# noinspection PyArgumentList
BaseType = enum.Enum('BaseType', 'Integer, Float, Double, Long, Reference')

_JAWA_BASES = {
    'D': BaseType.Double,
    'F': BaseType.Float,
    'J': BaseType.Long,
    'R': BaseType.Reference,
    'B': BaseType.Integer,
    'C': BaseType.Integer,
    'I': BaseType.Integer,
    'Z': BaseType.Integer,
}


@attr.s(frozen=True)
class ImpType:
    base = attr.ib(type=BaseType)
    dimensions = attr.ib(type=int)
    name = attr.ib(type=str, default=None)

    def is_array(self):
        return self.dimensions > 0

    def needs_two_slots(self):
        return self.base in (BaseType.Double, BaseType.Long)

    def is_reference_type(self):
        return self.base == BaseType.Reference

    def is_value_type(self):
        return not self.is_reference_type()

    @classmethod
    def from_jawa(cls, jawa_type: JVMType):
        base = _JAWA_BASES[jawa_type.base_type]
        if not base == BaseType.Reference:
            name = None
        else:
            name = jawa_type.name

        # noinspection PyArgumentList
        return cls(base, jawa_type.dimensions, name)

    @classmethod
    def integer(cls):
        # noinspection PyArgumentList
        return cls(BaseType.Integer, 0, None)

    @classmethod
    def float(cls):
        # noinspection PyArgumentList
        return cls(BaseType.Float, 0, None)

    @classmethod
    def long(cls):
        # noinspection PyArgumentList
        return cls(BaseType.Long, 0, None)

    @classmethod
    def double(cls):
        # noinspection PyArgumentList
        return cls(BaseType.Double, 0, None)

    @classmethod
    def reference(cls, name):
        # noinspection PyArgumentList
        return cls(BaseType.Reference, 0, name)

    @classmethod
    def array(cls, original_type, dimensions=1):
        # noinspection PyArgumentList
        return cls(original_type.base, dimensions, original_type.name)


@attr.s(frozen=True)
class Value:
    imp_type = attr.ib(type=ImpType)
    value = attr.ib(type=Any)
    is_null = attr.ib(init=False)

    def __attrs_post_init__(self):
        is_null = self.value == NULL
        if is_null and not self.imp_type.is_reference():
            raise TypeError('NULL values must be references')
        object.__setattr__(self, 'is_null', is_null)


class _NullClass:
    def __str__(self):
        return '<NullReference>'

    def __repr__(self):
        return str(self)


NULL = _NullClass()

_DEFAULT_VALUES = {
    BaseType.Integer: 0,
    BaseType.Long: 0,
    BaseType.Float: 0.0,
    BaseType.Double: 0.0,
    BaseType.Reference: NULL
}


def default_value(imp_type: ImpType):
    if imp_type.is_array():
        return NULL
    else:
        return _DEFAULT_VALUES[imp_type.base]


class JVMObject:
    @classmethod
    def from_class_file(cls, cf: ClassFile):
        fields = []
        for field in cf.fields:
            imp_type = ImpType.from_jawa(field.type)
            value = default_value(imp_type)
            name = field.name.value
            pair = name, Value(imp_type, value)
            fields.append(pair)

        return fields

    def __init__(self, fields: Mapping[str, Value]):
        self.fields = fields


class Locals:
    MISSING = object()

    def __init__(self, length):
        if length < 0:
            raise ValueError(f'{self.__class__.__name__} must have a positive length')
        self.length = length
        self._locals = [None] * length

    def store(self, index, value):
        if value is None:
            raise ValueError('Cannot store None in locals')
        self._locals[index] = value
        if value.imp_type.needs_two_slots():
            # noinspection PyTypeChecker
            self._locals[index + 1] = self.MISSING

    def load(self, index):
        result = self._locals[index]
        if result is None:
            raise ValueError(f'Access to uninitialized local variable at index {index}')
        if result is self.MISSING:
            message = f'Access to no-access local index {index}. Perhaps a previous value holds more than one index'
            raise ValueError(message)
        return result

    def init_with_parameters(self, parameters):
        index = 0
        for p in parameters:
            self.store(index, p)
            index += 1
            if p.imp_type.needs_two_slots():
                index += 1
