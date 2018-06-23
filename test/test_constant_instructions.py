from pyjvm.types import NULL_VALUE, Integer
from test.test_utils import BlankTestMachine


def test_a_const_null():
    machine = BlankTestMachine()
    machine.step_instruction('aconst_null')
    assert machine.current_op_stack().peek() == NULL_VALUE


def test_int_consts():
    machine = BlankTestMachine()
    for i in range(6):
        machine.step_instruction('iconst_' + str(i))
        assert machine.current_op_stack().peek() == Integer.create_instance(i)
