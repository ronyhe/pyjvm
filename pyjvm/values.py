from collections import namedtuple
# noinspection SpellCheckingInspection
from types import SimpleNamespace
from typing import Any

import attr

DESCRIPTOR_BASE_TYPES_THAT_ARE_ACTUALLY_INTEGERS = 'BCSIZ'

ImpType = namedtuple('ImpType', 'name, letter, double_index')


class ImpTypes(SimpleNamespace):
    Integer = ImpType('Integer', 'I', double_index=False)
    Float = ImpType('Float', 'F', double_index=False)
    Double = ImpType('Double', 'D', double_index=True)
    Long = ImpType('Long', 'J', double_index=True)
    Reference = ImpType('Reference', 'L', double_index=False)

    @classmethod
    def as_tuple(cls):
        return [cls.Integer, cls.Float, cls.Double, cls.Long, cls.Reference]

    @classmethod
    def from_letter(cls, letter):
        letter = letter.upper()
        if letter in DESCRIPTOR_BASE_TYPES_THAT_ARE_ACTUALLY_INTEGERS:
            return cls.Integer
        else:
            for imp in cls.as_list():
                if imp.letter == letter:
                    return imp

            raise ValueError(f'No implementation type for {letter}')


@attr.s(frozen=True)
class Value:
    imp_type = attr.ib(type=ImpType)
    value = attr.ib(type=Any)
    is_null = attr.ib(init=False)

    def __attrs_post_init__(self):
        is_null = self.value == _NULL_INSTANCE
        if is_null and not self.imp_type == ImpTypes.Reference:
            raise TypeError('NULL values must be references')
        object.__setattr__(self, 'is_null', is_null)


class _NullClass:
    def __str__(self):
        return '<NullReference>'

    def __repr__(self):
        return str(self)


_NULL_INSTANCE = _NullClass()

NULL = Value(ImpTypes.Reference, _NULL_INSTANCE)


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
        if value.imp_type.double_index:
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
            if p.imp_type.double_index:
                index += 1
