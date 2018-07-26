from typing import Dict

import attr

from pyjvm.model.jvm_types import JvmValue


@attr.s(frozen=True)
class JvmClass:
    name = attr.ib()
    name_of_base = attr.ib()
    constants = attr.ib()
    interfaces = attr.ib(converter=tuple, default=())
    fields = attr.ib(converter=dict, default=())
    methods = attr.ib(converter=dict, default=())
    static_fields = attr.ib(converter=dict, default=())


@attr.s(frozen=True)
class ExceptionHandler:
    start_pc = attr.ib()
    end_pc = attr.ib()
    handler_pc = attr.ib()
    catch_type = attr.ib()

    def relevant_to_pc(self, pc):
        return pc in range(self.start_pc, self.end_pc)


@attr.s(frozen=True)
class Handlers:
    handlers = attr.ib(converter=tuple, factory=tuple)

    def find_handlers(self, pc):
        return tuple(handler for handler in self.handlers if handler.relevant_to_pc(pc))


@attr.s(frozen=True)
class BytecodeMethod:
    max_locals = attr.ib(converter=int)
    max_stack = attr.ib(converter=int)
    instructions = attr.ib(converter=tuple)
    args = attr.ib(converter=tuple)
    exception_handlers = attr.ib(factory=Handlers)
    name = attr.ib(default='no_method_name')


@attr.s(frozen=True)
class MethodKey:
    name = attr.ib(type=str, converter=str)
    descriptor = attr.ib(type=str, converter=str)


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
