from pyjvm.types import NULL_VALUE
from test.test_utils import BlankTestMachine


def test_a_const_null():
    machine = BlankTestMachine()
    machine.step_instruction('aconst_null')
    assert machine.current_op_stack().peek() == NULL_VALUE
