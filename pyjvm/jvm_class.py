from typing import Tuple, Dict

from jawa.constants import ConstantPool
from jawa.util.bytecode import Instruction


class BytecodeMethod:
    def __init__(self, max_locals, max_stack, instructions):
        self.max_locals: int = int(max_locals)
        self.max_stack: int = int(max_stack)
        self.instructions: Tuple[Instruction] = tuple(instructions)


class Type:
    def __init__(self, name, *, default_value, refers_to=None, needs_two_slots=False):
        self.name: str = str(name)
        self.is_reference: bool = refers_to is not None
        self.is_value = not self.is_reference
        self.needs_two_slots: bool = bool(needs_two_slots)
        self.referenced_type = refers_to
        self.default_value = default_value
        self.is_reference_to_class = isinstance(refers_to, str)
        self.is_array_reference = isinstance(self, ArrayReferenceType)
        self.validate()

    def validate(self):
        if self.default_value is None:
            raise ValueError('Types must have default values')
        if self.is_reference and self.referenced_type is None:
            raise ValueError('Reference types must specify a referred type')

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


class _NullClass:
    def __repr__(self):
        return '<NULL>'


NULL = _NullClass()


class _ReferenceType(Type):
    def __init__(self, name, refers_to):
        super().__init__(name, refers_to=refers_to, default_value=NULL)


class ArrayReferenceType(_ReferenceType):
    def __init__(self, refers_to):
        super().__init__('<Array>', refers_to=refers_to)


class ObjectReferenceType(_ReferenceType):
    def __init__(self, refers_to):
        super().__init__('<Object>', refers_to=refers_to)


class JvmClass:
    def __init__(self, name, name_of_base, constants, names_of_interfaces=(), fields=(), methods=()):
        self.name: str = name
        self.name_of_base: str = name_of_base
        self.constants: ConstantPool = constants
        self.interface: Tuple[str] = tuple(names_of_interfaces)
        self.fields: Dict[str, Type] = dict(fields)
        self.methods: Dict[str, Method] = dict(methods)


class JvmValue:
    def __init__(self, type_, value):
        self.type: Type = type_
        self.value = value


class JvmObject:
    @classmethod
    def defaults(cls, field_specs):
        return cls(
            (name, type_.default_value) for name, type_ in dict(field_specs).items()
        )

    def __init__(self, fields):
        self.fields: Dict[str, JvmValue] = dict(fields)
