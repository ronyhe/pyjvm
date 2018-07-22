from pyjvm.actions import IncrementProgramCounter, Push, Pop, PushNewInstance, DuplicateTop, StoreInLocals, \
    StoreIntoArray, PutField, PutStatic, GoTo, Invoke
from pyjvm.machine import Machine, Frame
from pyjvm.model.frame_locals import Locals
from pyjvm.model.jvm_types import Integer, ArrayReferenceType
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


def test_duplicate_top():
    machine = dummy_machine()
    stack = machine.frames.peek().op_stack
    for index in reversed(range(10)):
        stack.push(Integer.create_instance(index))
    machine.act(DuplicateTop(amount_to_take=2, index_for_insertion=2))
    for _ in range(2):
        for i in range(2):
            assert stack.pop() == Integer.create_instance(i)


def test_store_in_locals():
    index = 1
    machine = act_on_dummy(StoreInLocals(
        index,
        SOME_INT
    ))
    assert machine.frames.peek().locals.load(index) == SOME_INT


def test_store_in_array():
    array_type = ArrayReferenceType(Integer)
    array_values = [Integer.create_instance(0) for _ in range(10)]

    array = array_type.create_instance(array_values)
    index = 3
    value = SOME_INT

    act_on_dummy(StoreIntoArray(
        array, index, value
    ))

    assert array_values[index] == value


def test_put_field():
    machine = dummy_machine()
    loader = machine.class_loader
    field_name = DUMMY_CLASS.instance_field.name.value

    instance = loader.default_instance(DUMMY_CLASS.name)

    assert not instance.value.fields[field_name] == SOME_INT
    machine.act(PutField(
        instance,
        field_name,
        SOME_INT
    ))

    assert instance.value.fields[field_name] == SOME_INT


def test_put_static():
    machine = dummy_machine()
    loader = machine.class_loader
    class_name = DUMMY_CLASS.name
    field_name = DUMMY_CLASS.class_field.name.value

    assert not loader.get_the_statics(class_name)[field_name] == SOME_INT
    machine.act(PutStatic(
        class_name,
        field_name,
        SOME_INT
    ))

    assert loader.get_the_statics(class_name)[field_name] == SOME_INT


def test_go_to():
    target = 15
    machine = act_on_dummy(GoTo(target))
    assert machine.frames.peek().pc == target


def test_invoke():
    machine = dummy_machine()
    class_name = DUMMY_CLASS.name
    method_name = DUMMY_CLASS.method.name.value
    arguments = [machine.class_loader.default_instance(DUMMY_CLASS.name)]

    machine.act(Invoke(
        class_name,
        method_name,
        arguments
    ))

    stack = machine.frames
    assert stack.size() == 2

    locals_ = stack.peek().locals
    assert locals_.load(0).type == DUMMY_CLASS.type
