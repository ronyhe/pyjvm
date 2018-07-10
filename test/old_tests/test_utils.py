from jawa.constants import ConstantPool
from jawa.util.bytecode import Instruction

from pyjvm.class_loaders import EmptyClassLoader
from pyjvm.frame_locals import Locals
from pyjvm.jvm_class import JvmClass
from pyjvm.machine import Frame, Machine
from pyjvm.stack import Stack


class BlankTestMachine(Machine):
    def __init__(self, class_loader=None):
        if class_loader is None:
            class_loader = EmptyClassLoader()
        super().__init__(class_loader)
        self.current_frame = Frame(JvmClass('SomeClass', 'SomeBase', ConstantPool()), Locals(5), Stack(), [])

    def step_instruction(self, *args):
        if len(args) == 1 and isinstance(args[0], Instruction):
            inst = args[0]
        else:
            inst = Instruction.create(*args)

        # noinspection PyProtectedMember
        inst = inst._replace(pos=0)
        self.current_frame.instructions = tuple([inst])
        self.run_frame(self.current_frame)
