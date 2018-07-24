from typing import Iterable

from jawa.util.bytecode import Instruction

from pyjvm.instructions.instructions import execute_instruction, InstructorInputs
from pyjvm.model.class_loaders import ClassLoader
from pyjvm.model.frame_locals import Locals
from pyjvm.model.hierarchies import is_value_instance_of
from pyjvm.model.jvm_class import BytecodeMethod, JvmClass, Handlers, MethodKey
from pyjvm.model.jvm_types import JvmValue
from pyjvm.model.stack import Stack
from pyjvm.utils.utils import class_as_descriptor


class Frame:
    @classmethod
    def from_class_and_method(cls, class_: JvmClass, method: BytecodeMethod):
        return cls(
            class_,
            Locals(method.max_locals),
            Stack(max_depth=method.max_stack),
            method.instructions,
            method_name=method.name
        )

    def __init__(self,
                 class_: JvmClass,
                 _locals: Locals,
                 op_stack: Stack[JvmValue],
                 instructions: Iterable[Instruction],
                 handlers=Handlers(),
                 pc=0,
                 method_name='no_method_name'):
        self.class_ = class_
        self.locals = _locals
        self.op_stack = op_stack
        self.instructions = tuple(instructions)
        self.handlers = handlers
        self.pc = pc
        self.method_name = method_name

    def next_instruction(self):
        for ins in self.instructions:
            if ins.pos >= self.pc:
                return ins

        raise IndexError('No more instructions')


class Unhandled(Exception):
    def __init__(self, instance):
        self.instance = instance


# noinspection PyUnusedLocal
def _default_echo(*args, **kwargs):
    pass


class Machine:
    def __init__(self, class_loader: ClassLoader, echo=None):
        self.class_loader = class_loader
        self.class_loader.first_load_function = self._first_class_load
        self.frames = Stack()
        self.echo = echo
        if self.echo is None:
            self.echo = _default_echo

    def run(self):
        while True:
            try:
                frame = self.frames.peek()
                instruction = frame.next_instruction()
            except IndexError:
                return
            else:
                self._run_instruction(instruction)

    def _run_instruction(self, instruction):
        frame = self.frames.peek()
        inputs = InstructorInputs(
            instruction=instruction,
            locals=frame.locals,
            op_stack=frame.op_stack,
            constants=frame.class_.constants,
            loader=self.class_loader
        )
        actions = execute_instruction(inputs)
        self.echo(f'{frame.class_.name}#{frame.method_name}, {instruction}')
        for action in actions:
            self.echo('\t' + str(action))
            self.act(action)

    def act(self, action):
        action_class = action.__class__.__name__
        snake_case = _to_snake_case(action_class)
        getattr(self, snake_case)(action)

    # noinspection PyUnusedLocal
    def _increment_program_counter(self, action):
        try:
            frame = self.frames.peek()
        except IndexError:
            return
        current_instruction = frame.next_instruction()
        frame.pc = current_instruction.pos + 1

    def _push(self, action):
        value = action.value
        self.frames.peek().op_stack.push(value)

    def _pop(self, action):
        amount = action.amount
        for _ in range(amount):
            self.frames.peek().op_stack.pop()

    def _push_new_instance(self, action):
        class_ = action.class_
        instance = self._create_instance(class_.name)
        self.frames.peek().op_stack.push(instance)

    def _duplicate_top(self, action):
        amount_to_take = action.amount_to_take
        index_for_insertion = action.index_for_insertion
        stack = self.frames.peek().op_stack

        values = stack.peek_many(amount_to_take)
        copies = [v.type.create_instance(v.value) for v in values]
        for copy in reversed(copies):
            stack.insert_at_offset(index_for_insertion, copy)

    def _store_in_locals(self, action):
        self.frames.peek().locals.store(action.index, action.value)

    # noinspection PyMethodMayBeStatic
    def _store_into_array(self, action):
        action.array.value[action.index] = action.value

    # noinspection PyMethodMayBeStatic
    def _put_field(self, action):
        action.object_.value.fields[action.field_name] = action.value

    def _put_static(self, action):
        self.class_loader.get_the_statics(action.class_name)[action.field_name] = action.value

    def _go_to(self, action):
        self.frames.peek().pc = action.target

    def _invoke(self, action):
        class_ = self.class_loader.get_the_class(action.class_name)
        method = class_.methods[action.method_key]
        frame = Frame.from_class_and_method(class_, method)
        for index, value in enumerate(action.arguments):
            frame.locals.store(index, value)

        self.frames.push(frame)
        if len(method.instructions) < 1:
            self._return_void(None)

    # noinspection PyUnusedLocal
    def _return_void(self, action):
        self.frames.pop()
        self._increment_program_counter(None)

    def _return_result(self, action):
        frames = self.frames
        frames.pop()
        frames.peek().op_stack.push(action.result)
        self._increment_program_counter(None)

    def _throw_object(self, action):
        self._throw_instance(action.value)

    def _create_and_throw(self, action):
        class_name = action.class_name
        instance = self._create_instance(class_name)
        self._throw_instance(instance)

    def _throw_instance(self, instance):
        frames = self.frames
        frame = frames.peek()
        handlers = frame.handlers.find_handlers(frame.pc)
        for handler in handlers:
            class_name = frame.class_.constants[handler.catch_type].name.value
            type_match = is_value_instance_of(instance, class_as_descriptor(class_name), self.class_loader)
            if type_match:
                frame.op_stack.push(instance)
                frame.pc = handler.handler_pc
                return

        frames.pop()
        if frames.size() == 0:
            raise Unhandled(instance)
        else:
            self._throw_instance(instance)

    def _create_instance(self, class_name):
        return self.class_loader.default_instance(class_name)

    def _first_class_load(self, class_):
        try:
            key = MethodKey('<clinit>', '()V')
            method = class_.methods[key]
        except KeyError:
            return
        temp_stack = Stack()
        temp_stack.push(Frame.from_class_and_method(class_, method))

        old_stack = self.frames
        self.frames = temp_stack
        self.run()
        self.frames = old_stack


def _to_snake_case(text):
    new_letters = [c if c.islower() else '_' + c.lower() for c in text]
    return ''.join(new_letters)


def run(loader, main_class_name, echo=None):
    class_ = loader.get_the_class(main_class_name)
    # noinspection SpellCheckingInspection
    key = MethodKey('main', '([Ljava/lang/String;)V')
    method = class_.methods[key]
    frame = Frame.from_class_and_method(class_, method)
    machine = Machine(loader, echo=echo)
    machine.frames.push(frame)
    machine.run()
