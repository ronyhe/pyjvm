from typing import Iterable

from jawa.util.bytecode import Instruction

from pyjvm.core.frame_locals import Locals
from pyjvm.core.jvm_class import JvmClass, BytecodeMethod, Handlers
from pyjvm.core.jvm_types import JvmValue
from pyjvm.core.stack import Stack


class Frame:
    """A runtime execution frame"""

    @classmethod
    def from_class_and_method(cls, class_: JvmClass, method: BytecodeMethod):
        return cls(
            class_,
            Locals(method.max_locals),
            Stack(max_depth=method.max_stack),
            method.instructions,
            method_name=method.name,
            method_descriptor=method.descriptor,
            exception_handlers=method.exception_handlers
        )

    def __init__(
            self,
            class_: JvmClass,
            _locals: Locals,
            op_stack: Stack[JvmValue],
            instructions: Iterable[Instruction],
            pc=0,
            method_name='no_method_name',
            method_descriptor='no_descriptor',
            exception_handlers=Handlers
    ):
        self.class_ = class_
        self.locals = _locals
        self.op_stack = op_stack
        self.instructions = tuple(instructions)
        self.pc = pc
        self.method_name = method_name
        self.method_descriptor = method_descriptor
        self.exception_handlers = exception_handlers

    def next_instruction(self):
        """Return the first instruction with `pos` greater or equal to `self.pc`"""
        for ins in self.instructions:
            if ins.pos >= self.pc:
                return ins

        raise IndexError('No more instructions')