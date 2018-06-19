from jawa.cf import ClassFile
from jawa.util.bytecode import Instruction, Operand, OperandTypes

from pyjvm.machine import Frame, Machine
from pyjvm.stack import Stack
from pyjvm.values import Locals, Value, ImpType


def blank_test_machine():
    frame = Frame(Locals(5), Stack(), [], 0)
    frames = Stack()
    frames.push(frame)
    # noinspection PyTypeChecker
    return Machine(ClassFile.create('TestClass'), frames, None)


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


class IntLoadTest(MachineTest):
    def __init__(self):
        super().__init__()
        self.integer_value = 6
        self.local_index = 0

    def set_up(self):
        self.machine.current_locals().store(self.local_index, Value(ImpType.integer(), self.integer_value))

    def create_instruction(self):
        # noinspection SpellCheckingInspection
        return Instruction.create('iload_0')

    def make_assertions(self):
        assert self.machine.current_op_stack().peek() == Value(ImpType.integer(), self.integer_value)


class IntLoadWithIndexTest(IntLoadTest):
    def __init__(self):
        super().__init__()
        self.index_constant = None

    def set_up(self):
        super().set_up()
        self.index_constant = self.machine.current_class.constants.create_integer(self.local_index)

    def create_instruction(self):
        # noinspection SpellCheckingInspection
        return Instruction.create('iload', [Operand(OperandTypes.CONSTANT_INDEX, self.index_constant.index)])


def test_classes():
    for test_class in [
        IntLoadTest,
        IntLoadWithIndexTest
    ]:
        test_class().run_test()
