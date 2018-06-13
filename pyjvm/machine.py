from jawa.methods import Method

from pyjvm.locals import Locals
from pyjvm.stack import Stack


class _Null:
    def __str__(self):
        return '<NullReference>'

    def __repr__(self):
        return str(self)


_NULL = _Null()


class Frame:
    def __init__(self, method: Method):
        code = method.code
        self.locals = Locals(code.max_locals)
        self.op_stack = Stack()
        self.instructions = tuple(code.disassemble())
        self.position = 0

    def next_instruction(self):
        for ins in self.instructions:
            if ins.pos >= self.position:
                return ins

        return None


class Machine:
    def __init__(self, initial_class, initial_method):
        self.current_class = initial_class
        self.frames = Stack()
        self.frames.push(Frame(initial_method))
        self.instruction = self.frames.peek().next_instruction()

    def step(self):
        execute_instruction(self, self.instruction)

    def run(self):
        while self.instruction is not None:
            self.step()
