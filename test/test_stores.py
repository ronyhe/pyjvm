from jawa.util.bytecode import Operand, OperandTypes

from pyjvm.types import Integer
from test.test_utils import BlankTestMachine


def test_int_store():
    machine = BlankTestMachine()
    value = Integer.create_instance(6)
    index = 1
    machine.current_op_stack().push(value)
    machine.step_instruction('istore', [Operand(OperandTypes.LITERAL, index)])
    assert machine.current_locals().load(index) == value


def test_int_store_0():
    machine = BlankTestMachine()
    value = Integer.create_instance(6)
    machine.current_op_stack().push(value)
    machine.step_instruction('istore_0')
    assert machine.current_locals().load(0) == value
