from jawa.constants import ConstantPool
from jawa.util.bytecode import Instruction

from pyjvm.class_loaders import ClassLoader
from pyjvm.frame_locals import Locals
from pyjvm.jvm_class import JvmClass
from pyjvm.machine import Frame, Machine
from pyjvm.stack import Stack


class BlankTestMachine(Machine):
    def __init__(self):
        # noinspection PyTypeChecker
        super().__init__(
            Stack([Frame(JvmClass('SomeClass', 'SomeBase', ConstantPool()), Locals(5), Stack(), [], 0)]),
            None,
            ClassLoader()
        )

    def step_instruction(self, *args):
        if len(args) == 1 and isinstance(args[0], Instruction):
            inst = args[0]
        else:
            inst = Instruction.create(*args)

        self.instruction = inst
        self.step()
