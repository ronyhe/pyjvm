from jawa.util.bytecode import Operand, OperandTypes

from pyjvm.jvm_types import Integer, RootObjectType, ArrayReferenceType, NULL_VALUE
from test.old_tests.test_utils import BlankTestMachine


def test_int_load():
    machine = BlankTestMachine()
    integer_value = Integer.create_instance(6)
    local_index = 0
    machine.current_locals().store(local_index, integer_value)
    machine.step_instruction('iload_0')
    assert machine.current_op_stack().peek() == integer_value


def test_ref_load():
    machine = BlankTestMachine()
    value = NULL_VALUE
    local_index = 2
    machine.current_locals().store(local_index, value)
    machine.step_instruction('aload_2')
    assert machine.current_op_stack().peek() == value


def test_ref_load_with_index():
    machine = BlankTestMachine()
    value = NULL_VALUE
    local_index = 2
    machine.current_locals().store(local_index, value)
    machine.step_instruction('aload', [Operand(OperandTypes.LITERAL, 2)])
    assert machine.current_op_stack().peek() == value


def test_load_ref_from_array():
    array_type = ArrayReferenceType(refers_to=RootObjectType)
    array = array_type.create_instance([NULL_VALUE])

    machine = BlankTestMachine()
    stack = machine.current_op_stack()
    stack.push(array)

    stack.push(Integer.create_instance(0))
    machine.step_instruction('aaload')

    assert stack.size() == 1
    assert stack.peek() == NULL_VALUE
