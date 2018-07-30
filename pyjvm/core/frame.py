from typing import Iterable

import attr
from jawa.util.bytecode import Instruction

from pyjvm.core.frame_locals import Locals
from pyjvm.core.jvm_class import JvmClass, BytecodeMethod, Handlers
from pyjvm.core.jvm_types import JvmValue
from pyjvm.core.stack import Stack


@attr.s
class Frame:
    """A runtime execution frame"""
    jvm_class = attr.ib(type=JvmClass)
    method_name = attr.ib(type=str)
    method_descriptor = attr.ib(type=str)
    instructions = attr.ib(type=Iterable[Instruction], converter=tuple)
    locals = attr.ib(type=Locals)
    op_stack = attr.ib(type=Stack[JvmValue])
    exception_handlers = attr.ib(type=Handlers)
    pc = attr.ib(type=int, default=0)

    @classmethod
    def from_class_and_method(cls, jvm_class: JvmClass, method: BytecodeMethod):
        return cls(
            jvm_class=jvm_class,
            method_name=method.name,
            method_descriptor=method.descriptor,
            instructions=method.instructions,
            locals=Locals(method.max_locals),
            op_stack=Stack(max_depth=method.max_stack),
            exception_handlers=method.exception_handlers
        )

    def next_instruction(self):
        """Return the first instruction with `pos` greater or equal to `self.pc`"""
        for ins in self.instructions:
            if ins.pos >= self.pc:
                return ins

        raise IndexError('No more instructions')
