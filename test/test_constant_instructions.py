from pyjvm.types import NULL_VALUE, Integer, Double
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


def test_double_consts():
    machine = BlankTestMachine()
    machine.step_instruction('dconst_0')
    assert machine.current_op_stack().peek() == Double.create_instance(0.0)
