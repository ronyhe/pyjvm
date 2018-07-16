from typing import Dict

import attr

from pyjvm.jvm_types import JvmValue

# noinspection SpellCheckingInspection
NAME_OF_STATIC_CONSTRUCTOR = 'clinit'


@attr.s(frozen=True)
class BytecodeMethod:
    max_locals = attr.ib(converter=int)
    max_stack = attr.ib(converter=int)
    instructions = attr.ib(converter=tuple)
    args = attr.ib(converter=tuple)


@attr.s(frozen=True)
class JvmClass:
    name = attr.ib()
    name_of_base = attr.ib()
    constants = attr.ib()
    interfaces = attr.ib(converter=tuple, default=())
    fields = attr.ib(converter=dict, default=())
    methods = attr.ib(converter=dict, default=())
    static_fields = attr.ib(converter=dict, default=())


class JvmObject:
    @classmethod
    def defaults(cls, field_specs):
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
        return f'{self.__class__.__name__}({repr(self.fields)})'
