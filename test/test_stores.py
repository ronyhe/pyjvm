from jawa.util.bytecode import Operand, OperandTypes

from pyjvm.types import Integer, NULL_VALUE
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


def test_a_store():
    machine = BlankTestMachine()
    value = NULL_VALUE
    index = 1
    machine.current_op_stack().push(value)
    machine.step_instruction('astore', [Operand(OperandTypes.LITERAL, index)])
    assert machine.current_locals().load(index) == value
