from typing import Iterable

from jawa.cf import ClassFile
from jawa.constants import ConstantPool
from jawa.methods import Method
from jawa.util.bytecode import Instruction

from pyjvm.execution.execution import execute_instruction
from pyjvm.values import Value, Locals
from pyjvm.stack import Stack


class Frame:
    @classmethod
    def from_method(cls, method: Method):
        code = method.code
        _locals = Locals(code.max_locals)
        op_stack = Stack(code.max_stack)
        instructions = code.disassemble()
        return cls(_locals, op_stack, instructions, 0)

    def __init__(self, _locals: Locals, op_stack: Stack[Value], instructions: Iterable[Instruction], position: int):
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
    def from_class_and_method(cls, the_class: ClassFile, method: Method):
        frame = Frame.from_method(method)
        frames = Stack()
        frames.push(frame)
        instruction = frame.next_instruction()
        return cls(the_class, frames, instruction)

    def __init__(self, current_class: ClassFile, frames: Stack[Frame], instruction: Instruction):
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

    def current_op_stack(self):
        return self.current_frame().op_stack

    def current_constants(self) -> ConstantPool:
        return self.current_class.constants
