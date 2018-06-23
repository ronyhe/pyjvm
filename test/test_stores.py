from jawa.util.bytecode import Operand, OperandTypes

from pyjvm.types import Integer, NULL_VALUE, ArrayReferenceType
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


def test_int_array_store():
    machine = BlankTestMachine()
    stack = machine.current_op_stack()

    value = Integer.create_instance(6)
    index = Integer.create_instance(0)
    array_ref = ArrayReferenceType(Integer).create_instance([0])

    stack.push(array_ref)
    stack.push(index)
    stack.push(value)

    machine.step_instruction('iastore')
    assert array_ref.value[0] == value
