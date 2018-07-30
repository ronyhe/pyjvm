"""Test that the Action instances have the correct effects on a Machine

Some of the actions require a complete run configuration with relating attributes.
For example, to test exception throwing, the class of the exception instance muse be available in the class loader.
However, actual standard library classes are too complex to manage in these tests.
One needs to scan the library to find classes that specifically adhere to the test criteria.
And even if we find them, they'll have a lot of incidental information.

This is the reason for the fairly large amounts of constants at the top of the module.
They defined a complete JvmClass and ClassLoader configuration that answers the need of all the tests in the module.

While this may seem a bit intimidating at first,
it is completely declarative, and will (hopefully) become obvious once one gets to know
the types in the system.
"""
import pytest
from jawa.constants import ConstantPool
from jawa.util.bytecode import Instruction

from pyjvm.core.actions import Push, Pop, PushNewInstance, DuplicateTop, StoreInLocals, \
    StoreIntoArray, PutField, PutStatic, GoTo, Invoke, ReturnVoid, ReturnResult, ThrowObject, CreateAndThrow, \
    IncrementProgramCounter
from pyjvm.core.class_loaders import FixedClassLoader
from pyjvm.core.frame import Frame
from pyjvm.core.jvm_class import Handlers, ExceptionHandler, JvmClass, MethodKey, BytecodeMethod
from pyjvm.core.jvm_types import Integer, ArrayReferenceType, RootObjectType, ObjectReferenceType
from pyjvm.core.machine import Machine, Unhandled, NativeNotSupported
from pyjvm.utils.utils import named_tuple_replace
from test.utils import SOME_INT

COMPLEX_CLASS_NAME = 'class_name'
EXCEPTION_NAME = 'some_exception'
FIELD_NAME = 'some_field'
FIELD_DESCRIPTOR = 'I'
METHOD_NAME = 'some_method'
METHOD_DESCRIPTOR = '(II)I'
METHOD_KEY = MethodKey(METHOD_NAME, METHOD_DESCRIPTOR)
HANDLER = ExceptionHandler(
    start_pc=2,
    end_pc=3,
    handler_pc=4,
    catch_type=EXCEPTION_NAME
)

METHOD = BytecodeMethod(
    name='method_name',
    descriptor='(II)V',
    instructions=[
        named_tuple_replace(Instruction.create('nop'), pos=i) for i in range(5)
    ],
    max_locals=5,
    max_stack=15,
    args=[Integer, Integer],
    exception_handlers=Handlers([HANDLER])
)

COMPLEX_CLASS = JvmClass(
    name=COMPLEX_CLASS_NAME,
    name_of_base=RootObjectType.refers_to,
    constants=ConstantPool(),
    fields={
        FIELD_NAME: Integer
    },
    static_fields={
        FIELD_NAME: Integer
    },
    methods={
        METHOD_KEY: METHOD
    }
)


def complex_machine():
    machine = Machine(FixedClassLoader({
        COMPLEX_CLASS_NAME: COMPLEX_CLASS,
        EXCEPTION_NAME: JvmClass(
            name=EXCEPTION_NAME,
            name_of_base=RootObjectType.refers_to,
            constants=ConstantPool()
        ),
        RootObjectType.refers_to: JvmClass(
            name=RootObjectType.refers_to,
            name_of_base=None,
            constants=ConstantPool()
        )
    }))
    for _ in range(2):
        frame = Frame.from_class_and_method(COMPLEX_CLASS, METHOD)
        machine.frames.push(frame)
    return machine


def test_increment_program_counter():
    machine = complex_machine()
    machine.act(IncrementProgramCounter())
    assert machine.frames.peek().pc == 1


def test_push():
    machine = complex_machine()
    machine.act(Push(SOME_INT))
    assert machine.frames.peek().op_stack.peek() == SOME_INT


def test_pop():
    machine = complex_machine()
    stack = machine.frames.peek().op_stack
    stack.push(SOME_INT)
    stack.push(SOME_INT)
    machine.act(Pop(2))
    assert stack.size() == 0


def test_push_new_instance():
    machine = complex_machine()
    machine.act(
        PushNewInstance(COMPLEX_CLASS)
    )
    stack = machine.frames.peek().op_stack
    assert stack.peek().type == ObjectReferenceType(COMPLEX_CLASS_NAME)


def test_duplicate_top():
    machine = complex_machine()
    stack = machine.frames.peek().op_stack
    for index in reversed(range(10)):
        stack.push(Integer.create_instance(index))
    machine.act(DuplicateTop(amount_to_take=2, index_for_insertion=2))
    for _ in range(2):
        for i in range(2):
            assert stack.pop() == Integer.create_instance(i)


def test_store_in_locals():
    index = 1
    machine = complex_machine()
    machine.act(StoreInLocals(
        index, SOME_INT
    ))
    assert machine.frames.peek().locals.load(index) == SOME_INT


def test_store_in_array():
    array_type = ArrayReferenceType(Integer)
    array_values = [Integer.create_instance(0) for _ in range(10)]

    array = array_type.create_instance(array_values)
    index = 3
    value = SOME_INT

    machine = complex_machine()
    machine.act(StoreIntoArray(
        array, index, value
    ))

    assert array_values[index] == value


def test_put_field():
    machine = complex_machine()
    instance = machine.class_loader.default_instance(COMPLEX_CLASS_NAME)
    assert not instance.value.fields[FIELD_NAME] == SOME_INT

    machine.act(PutField(
        instance,
        FIELD_NAME,
        SOME_INT
    ))

    assert instance.value.fields[FIELD_NAME] == SOME_INT


def test_put_static():
    machine = complex_machine()
    loader = machine.class_loader
    statics = loader.get_the_statics(COMPLEX_CLASS_NAME)

    assert not statics[FIELD_NAME] == SOME_INT

    machine.act(PutStatic(
        COMPLEX_CLASS_NAME,
        FIELD_NAME,
        SOME_INT
    ))

    assert statics[FIELD_NAME] == SOME_INT


def test_go_to():
    target = HANDLER.handler_pc
    machine = complex_machine()
    frame = machine.frames.peek()

    assert not frame.pc == target
    machine.act(GoTo(target))
    assert frame.pc == target


def test_invoke():
    machine = complex_machine()
    initial_frame_count = machine.frames.size()
    machine.act(Invoke(
        COMPLEX_CLASS_NAME,
        METHOD_KEY,
        [SOME_INT, SOME_INT, SOME_INT]
    ))
    assert machine.frames.size() == initial_frame_count + 1
    local = machine.frames.peek().locals
    for i in range(3):
        assert local.load(i) == SOME_INT


def test_return_void():
    machine = complex_machine()
    initial_frame_count = machine.frames.size()
    machine.act(ReturnVoid())
    assert machine.frames.size() == initial_frame_count - 1
    assert machine.frames.peek().op_stack.size() == 0


def test_return_result():
    machine = complex_machine()
    frames = machine.frames
    initial_frame_count = frames.size()

    machine.act(ReturnResult(SOME_INT))

    assert frames.size() == initial_frame_count - 1
    assert frames.peek().op_stack.peek() == SOME_INT


def test_throw_object():
    machine = complex_machine()
    instance = machine.class_loader.default_instance(EXCEPTION_NAME)
    with pytest.raises(Unhandled):
        machine.act(ThrowObject(instance))


def test_throw_with_handler():
    machine = complex_machine()
    frames = machine.frames
    next_frame = frames.peek(1)

    next_frame.pc = HANDLER.start_pc
    instance = machine.class_loader.default_instance(EXCEPTION_NAME)
    machine.act(ThrowObject(instance))

    assert frames.peek() is next_frame
    assert frames.peek().pc == HANDLER.handler_pc


def test_create_and_throw():
    machine = complex_machine()
    try:
        machine.act(CreateAndThrow(COMPLEX_CLASS_NAME))
    except Unhandled as ex:
        assert ex.instance.type.refers_to == COMPLEX_CLASS_NAME
    else:
        pytest.fail()


def test_native_method(std_loader):
    machine = Machine(std_loader)
    action = Invoke(
        'java/lang/System',
        MethodKey(
            'currentTimeMillis',
            '()J'
        ),
        []
    )
    with pytest.raises(NativeNotSupported):
        machine.act(action)
