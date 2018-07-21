from typing import Iterable

from jawa.util.bytecode import Instruction

from pyjvm.model.class_loaders import ClassLoader
from pyjvm.model.frame_locals import Locals
from pyjvm.model.jvm_class import BytecodeMethod, JvmClass
from pyjvm.model.jvm_types import JvmValue
from pyjvm.model.stack import Stack


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
                 instructions: Iterable[Instruction],
                 pc=0):
        self.class_ = class_
        self.locals = _locals
        self.op_stack = op_stack
        self.instructions = tuple(instructions)
        self.pc = pc

    def next_instruction(self):
        for ins in self.instructions:
            if ins.pos >= self.pc:
                return ins

        raise IndexError('No more instructions')


def _to_snake_case(text):
    new_letters = [c if c.islower() else '_' + c.lower() for c in text]
    return ''.join(new_letters)


class Machine:
    def __init__(self, class_loader: ClassLoader):
        self.class_loader = class_loader
        self.frames = Stack()

    def act(self, action):
        action_class = action.__class__.__name__
        snake_case = _to_snake_case(action_class)
        getattr(self, snake_case)(action)

    # noinspection PyUnusedLocal
    def _increment_program_counter(self, action):
        self.frames.peek().pc += 1

    def _push(self, action):
        value = action.value
        self.frames.peek().op_stack.push(value)

    def _pop(self, action):
        amount = action.amount
        for _ in range(amount):
            self.frames.peek().op_stack.pop()
