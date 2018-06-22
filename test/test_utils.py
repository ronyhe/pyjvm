from jawa.constants import ConstantPool

from pyjvm.frame_locals import Locals
from pyjvm.jvm_class import JvmClass
from pyjvm.machine import Frame, Machine
from pyjvm.stack import Stack


def blank_test_machine():
    frame = Frame(Locals(5), Stack(), [], 0)
    frames = Stack()
    frames.push(frame)
    # noinspection PyTypeChecker
    return Machine(JvmClass('SomeClass', 'SomeBase', ConstantPool()), frames, None)


class MachineTest:
    def __init__(self):
        self.machine = blank_test_machine()

    def set_up(self):
        pass

    def create_instruction(self):
        raise NotImplementedError()

    def make_assertions(self):
        raise NotImplementedError()

    def run_test(self):
        self.set_up()
        self.machine.instruction = self.create_instruction()
        self.machine.step()
        self.make_assertions()

    def __repr__(self):
        return f'<{self.__class__.__name__}>'
