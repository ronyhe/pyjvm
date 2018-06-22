from typing import Iterable

from jawa.constants import ConstantPool
from jawa.util.bytecode import Instruction

from pyjvm.execution.execution import execute_instruction
from pyjvm.frame_locals import Locals
from pyjvm.jvm_class import BytecodeMethod, JvmClass
from pyjvm.stack import Stack
from pyjvm.values import JvmValue


class Frame:
    @classmethod
    def from_method(cls, method: BytecodeMethod):
        return cls(
            Locals(method.max_locals),
            Stack(method.max_stack),
            method.instructions,
            0
        )

    def __init__(self, _locals: Locals, op_stack: Stack[JvmValue], instructions: Iterable[Instruction], position: int):
        self.locals = _locals
        self.op_stack = op_stack
        self.instructions = tuple(instructions)
        self.position = position

    def next_instruction(self):
        for ins in self.instructions:
            if ins.pos >= self.position:
                return ins

        return None


class Machine:
    @classmethod
    def from_class_and_method(cls, the_class: JvmClass, method: BytecodeMethod):
        frame = Frame.from_method(method)
        frames = Stack()
        frames.push(frame)
        instruction = frame.next_instruction()
        return cls(the_class, frames, instruction)

    def __init__(self, current_class: JvmClass, frames: Stack[Frame], instruction: Instruction):
        self.current_class = current_class
        self.frames = frames
        self.instruction = instruction

    def step(self):
        execute_instruction(self.instruction, self)

    def run(self):
        while self.instruction is not None:
            self.step()

    def current_frame(self) -> Frame:
        return self.frames.peek()

    def current_locals(self) -> Locals:
        return self.current_frame().locals

    def current_op_stack(self) -> Stack[JvmValue]:
        return self.current_frame().op_stack

    def current_constants(self) -> ConstantPool:
        return self.current_class.constants
