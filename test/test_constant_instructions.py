from jawa.util.bytecode import Instruction

from pyjvm.jvm_class import NullReference
from test.test_utils import blank_test_machine


def test_a_const_null():
    machine = blank_test_machine()
    # noinspection SpellCheckingInspection
    machine.instruction = Instruction.create('aconst_null')
    machine.step()
    assert machine.current_op_stack().peek() == NullReference
