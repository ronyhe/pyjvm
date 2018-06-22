from jawa.util.bytecode import Instruction, Operand, OperandTypes

from pyjvm.jvm_class import Integer, JvmValue, ArrayReferenceType, RootObjectType, NullReference
from test.test_utils import MachineTest


class IntLoadTest(MachineTest):
    def __init__(self):
        super().__init__()
        self.integer_value = 6
        self.local_index = 0

    def set_up(self):
        self.machine.current_locals().store(self.local_index, JvmValue(Integer, self.integer_value))

    def create_instruction(self):
        # noinspection SpellCheckingInspection
        return Instruction.create('iload_0')

    def make_assertions(self):
        assert self.machine.current_op_stack().peek() == JvmValue(Integer, self.integer_value)


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


class LoadReferenceFromArrayTest(MachineTest):
    def set_up(self):
        super().set_up()
        array_type = ArrayReferenceType(refers_to=RootObjectType)
        array = JvmValue(array_type, [NullReference])

        stack = self.machine.current_op_stack()
        stack.push(array)
        stack.push(JvmValue(Integer, 0))

    def create_instruction(self):
        # noinspection SpellCheckingInspection
        return Instruction.create('aaload')

    def make_assertions(self):
        stack = self.machine.current_op_stack()
        assert stack.size() == 1
        assert stack.peek() == NullReference