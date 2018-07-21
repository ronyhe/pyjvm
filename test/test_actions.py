from pyjvm.actions import IncrementProgramCounter, Push, Pop, PushNewInstance
from pyjvm.machine import Machine, Frame
from pyjvm.model.frame_locals import Locals
from pyjvm.model.stack import Stack
from pyjvm.utils.jawa_conversions import convert_class_file
from test.utils import dummy_loader, DUMMY_CLASS, SOME_INT

DUMMY_AS_JVM_CLASS = convert_class_file(DUMMY_CLASS.class_file)


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
    machine = act_on_dummy(Push(SOME_INT))
    actual = machine.frames.peek().op_stack.peek()
    assert actual == SOME_INT


def test_pop():
    machine = dummy_machine()
    stack = machine.frames.peek().op_stack
    stack.push(SOME_INT)
    stack.push(SOME_INT)
    machine.act(Pop(2))
    assert stack.size() == 0


def test_push_new_instance():
    machine = act_on_dummy(PushNewInstance(DUMMY_AS_JVM_CLASS))
    stack = machine.frames.peek().op_stack
    assert stack.peek().type == DUMMY_CLASS.type
