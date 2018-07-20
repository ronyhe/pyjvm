from typing import Iterable

from jawa.util.bytecode import Instruction

from pyjvm.class_loaders import ClassLoader
from pyjvm.frame_locals import Locals
from pyjvm.jvm_class import BytecodeMethod, JvmClass
from pyjvm.jvm_types import JvmValue
from pyjvm.stack import Stack


class Frame:
    @classmethod
    def from_class_and_method(cls, class_: JvmClass, method: BytecodeMethod):
        return cls(
            class_,
            Locals(method.max_locals),
            Stack(max_depth=method.max_stack),
            method.instructions
        )

    def __init__(self,
                 class_: JvmClass,
                 _locals: Locals,
                 op_stack: Stack[JvmValue],
                 instructions: Iterable[Instruction]):
        self.class_ = class_
        self.locals = _locals
        self.op_stack = op_stack
        self.instructions = tuple(instructions)

    def next_instruction(self, pc):
        for ins in self.instructions:
            if ins.pos >= pc:
                return ins

        return None


class Machine:
    def __init__(self, class_loader: ClassLoader):
        self.current_frame: Frame = None
        self.class_loader = class_loader
