from pyjvm.actions import IncrementProgramCounter, Push
from pyjvm.machine import Machine, Frame
from pyjvm.model.frame_locals import Locals
from pyjvm.model.jvm_types import Integer
from pyjvm.model.stack import Stack
from pyjvm.utils.jawa_conversions import convert_class_file
from test.utils import dummy_loader, DUMMY_CLASS


def dummy_machine():
    machine = Machine(dummy_loader())
    frame = Frame(convert_class_file(DUMMY_CLASS.class_file), Locals(5), Stack(), [])
    machine.frames.push(frame)
    return machine


def act_on_dummy(action):
    machine = dummy_machine()
    machine.act(action)
    return machine


def test_increment_program_counter():
    machine = act_on_dummy(IncrementProgramCounter())
    assert machine.frames.peek().pc == 1


def test_push():
    value = Integer.create_instance(1)
    machine = act_on_dummy(Push(value))
    actual = machine.frames.peek().op_stack.peek()
    assert actual == value
