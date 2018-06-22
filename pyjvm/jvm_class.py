from typing import Tuple, Dict

from jawa.constants import ConstantPool
from jawa.util.bytecode import Instruction

from pyjvm.types import Type, JvmValue


class BytecodeMethod:
    def __init__(self, max_locals, max_stack, instructions):
        self.max_locals: int = int(max_locals)
        self.max_stack: int = int(max_stack)
        self.instructions: Tuple[Instruction] = tuple(instructions)


class JvmClass:
    def __init__(self, name, name_of_base, constants, names_of_interfaces=(), fields=(), methods=()):
        self.name: str = name
        self.name_of_base: str = name_of_base
        self.constants: ConstantPool = constants
        self.interface: Tuple[str] = tuple(names_of_interfaces)
        self.fields: Dict[str, Type] = dict(fields)
        self.methods: Dict[str, BytecodeMethod] = dict(methods)


class JvmObject:
    @classmethod
    def defaults(cls, field_specs):
        return cls(
            (name, type_.default_value) for name, type_ in dict(field_specs).items()
        )

    def __init__(self, fields):
        self.fields: Dict[str, JvmValue] = dict(fields)
