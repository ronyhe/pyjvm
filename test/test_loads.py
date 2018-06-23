from pyjvm.types import Integer, RootObjectType, ArrayReferenceType, NULL_VALUE
from test.test_utils import BlankTestMachine


def test_int_load():
    machine = BlankTestMachine()
    integer_value = Integer.create_instance(6)
    local_index = 0
    machine.current_locals().store(local_index, integer_value)
    machine.step_instruction('iload_0')
    assert machine.current_op_stack().peek() == integer_value


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
