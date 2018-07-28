from typing import Dict

import attr

from pyjvm.model.jvm_types import JvmValue


@attr.s(frozen=True)
class JvmClass:
    """A class at runtime

    name: str, the name of this class
    name_of_base: str, the name of the super class
    interfaces: Iterable[str], the names of the interfaces this class implements
    fields: Mapping[str, JvmType], the names and types of the instance fields in this class
    methods: Mapping[MethodKey, BytecodeMethod], the keys and corresponding methods in this class
    static_fields: Mapping[str, JvmType], the names and types of the static fields in this class

    Note that `fields` holds only instance fields, static fields go into `static_fields`.
    However, `methods` holds all methods, including static methods.
    """
    name = attr.ib()
    name_of_base = attr.ib()
    constants = attr.ib()
    interfaces = attr.ib(converter=tuple, default=())
    fields = attr.ib(converter=dict, default=())
    methods = attr.ib(converter=dict, default=())
    static_fields = attr.ib(converter=dict, default=())


@attr.s(frozen=True)
class ExceptionHandler:
    """Description of a method exception handler.

    The information in this class is similar to the content of
    the exception_table entries described in the section 4.7.3 of the JVM 8 spec.

    start_pc: int, the index of the instruction at which this handler becomes relevant. Inclusive
    end_pc: int, the index of the instruction at which this handler stops being relevant. Exclusive
    handler_pc: int, the index of the first instruction of exception handling code.
      In Java terms, the location of the catch clause.
    catch_type: The type of exception to which this handler is relevant.
    """
    start_pc = attr.ib()
    end_pc = attr.ib()
    handler_pc = attr.ib()
    catch_type = attr.ib()

    def relevant_to_pc(self, pc):
        """Return True if this handler should handle exception thrown at `pc`, False otherwise."""
        return pc in range(self.start_pc, self.end_pc)


@attr.s(frozen=True)
class Handlers:
    """A collection of `ExceptionHandler` objects.

    The JVM 8 specification states that the order of handlers matters.
    This class does not change the order and respect it in lookups.
    """
    handlers = attr.ib(converter=tuple, factory=tuple)

    def find_handlers(self, pc):
        """Return the handlers that are relevant to `pc`, in order"""
        return tuple(handler for handler in self.handlers if handler.relevant_to_pc(pc))


@attr.s(frozen=True)
class BytecodeMethod:
    """A JVM method

    max_locals: int, the size of the Locals array
    max_stack: int, the maximum size of the frame's op stack
    instructions: Iterable[Instruction], the instructions for this method
    args: Iterable[JvmType], the types of arguments this method expects.
    exception_handler: Handlers, the exception handlers of the method. Defaults to an empty Handlers object.
    name: str, this method's name
    """
    max_locals = attr.ib(converter=int)
    max_stack = attr.ib(converter=int)
    instructions = attr.ib(converter=tuple)
    args = attr.ib(converter=tuple)
    exception_handlers = attr.ib(factory=Handlers)
    name = attr.ib(default='no_method_name')
    is_native = attr.ib(default=False, converter=bool)


@attr.s(frozen=True)
class MethodKey:
    """A lookup key for methods

    JVM overload rules state that a class can have more than one method with the same name.
    A method is unique only in relation to their name *and* its descriptor.

    name: str, method name
    descriptor: str, method descriptor
    """
    name = attr.ib(type=str, converter=str)
    descriptor = attr.ib(type=str, converter=str)


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
        return f'{self.__class__.__name__}({repr(self.fields)})'
