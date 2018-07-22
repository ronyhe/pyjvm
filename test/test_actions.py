import pytest

from pyjvm.actions import Push, Pop, PushNewInstance, DuplicateTop, StoreInLocals, \
    StoreIntoArray, PutField, PutStatic, GoTo, Invoke, ReturnVoid, ReturnResult, ThrowObject, CreateAndThrow
from pyjvm.machine import Machine, Frame, Unhandled
from pyjvm.model.frame_locals import Locals
from pyjvm.model.jvm_class import Handlers, ExceptionHandler
from pyjvm.model.jvm_types import Integer, ArrayReferenceType
from pyjvm.model.stack import Stack
from pyjvm.utils.jawa_conversions import convert_class_file
from test.utils import dummy_loader, DUMMY_CLASS, SOME_INT


def dummy_as_jvm_class():
    return convert_class_file(DUMMY_CLASS.class_file)


def dummy_frame():
    return Frame(convert_class_file(DUMMY_CLASS.class_file), Locals(5), Stack(), [])


def dummy_machine():
    machine = Machine(dummy_loader())
    frame = dummy_frame()
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
    machine = act_on_dummy(PushNewInstance(dummy_as_jvm_class()))
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


def test_return_void():
    machine = dummy_machine()
    frames = machine.frames
    frames.push(dummy_frame())
    assert frames.size() == 2
    machine.act(ReturnVoid())
    assert frames.size() == 1
    assert frames.peek().op_stack.size() == 0


def test_return_result():
    machine = dummy_machine()
    frames = machine.frames
    frames.push(dummy_frame())
    machine.act(ReturnResult(SOME_INT))
    ops = frames.peek().op_stack
    assert frames.size() == 1
    assert ops.size() == 1
    assert ops.peek() == SOME_INT


def test_throw_object():
    machine = dummy_machine()
    instance = machine.class_loader.default_instance(DUMMY_CLASS.name)
    with pytest.raises(Unhandled):
        machine.act(ThrowObject(instance))


def test_throw_with_handler():
    machine = dummy_machine()
    class_ = dummy_as_jvm_class()
    class_constant = class_.constants.create_class(DUMMY_CLASS.name)

    handler_pc = 8
    frame_with_handler = Frame(
        dummy_as_jvm_class(),
        Locals(5),
        Stack(),
        [],
        Handlers([
            ExceptionHandler(
                start_pc=0,
                end_pc=1,
                handler_pc=handler_pc,
                catch_type=class_constant.index
            )
        ])
    )

    frame_that_throws = dummy_frame()

    frames = machine.frames
    frames.push(frame_with_handler)
    frames.push(frame_that_throws)

    instance = machine.class_loader.default_instance(DUMMY_CLASS.name)
    machine.act(ThrowObject(instance))

    assert frames.size() == 2

    top_frame = frames.peek()
    assert top_frame is frame_with_handler
    assert top_frame.pc == handler_pc

    op_stack = top_frame.op_stack
    assert op_stack.size() == 1
    assert op_stack.peek() == instance


def test_create_and_throw():
    machine = dummy_machine()
    try:
        machine.act(CreateAndThrow(DUMMY_CLASS.name))
    except Unhandled as ex:
        assert ex.instance.type == DUMMY_CLASS.type
    else:
        pytest.fail()
