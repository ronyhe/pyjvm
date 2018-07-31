from pyjvm.core.class_loaders import ClassLoader
from pyjvm.core.frame import Frame
from pyjvm.core.hierarchies import is_value_instance_of
from pyjvm.core.jvm_class import MethodKey
from pyjvm.core.stack import Stack
from pyjvm.instructions.instructions import execute_instruction, InstructorInputs
from pyjvm.utils.utils import class_as_descriptor


class Unhandled(Exception):
    """An JVM exception propagated all the way up"""

    def __init__(self, instance):
        self.instance = instance


class NativeNotSupported(Exception):
    def __init__(self, message):
        super().__init__(message)


class Machine:
    """A JVM

    In other words, an object that runs JVM class files.

    See the `act` method documentation for information in how actions are dispatched to their corresponding method.

    Many of the action methods are `self` explanatory when taken together with the corresponding Action sub class.
    See action.py for more information.
    See what I did there? With the `self`? lol

    The actions `Invoke`, `ThrowObject` and `CreateAndThrow` need not be used with the `IncrementProgramCounter` action.
    See the corresponding methods `_invoke`, `_throw_object` and `_create_and_throw` for the implementation details
    that handle the program counter in these situations.
    """

    def __init__(self, class_loader: ClassLoader, echo=None):
        """Return a new Machine instance

        Note that Machine will change the `class_loader.first_load_function`
        :param class_loader: the ClassLoader this machine should use
        :param echo: A `print` like function for reports during execution
        """
        self.class_loader = class_loader
        self.class_loader.first_load_function = self._first_class_load
        self.frames = Stack()
        self.echo = echo
        if self.echo is None:
            self.echo = _default_echo

    def run(self):
        """Start running"""
        while True:
            try:
                frame = self.frames.peek()
                instruction = frame.next_instruction()
            except IndexError:
                # If there are no more frames, or no more instructions - we're done
                return
            else:
                self._run_instruction(instruction)

    def _run_instruction(self, instruction):
        """Translate `instruction` into `Actions` and execute them"""
        frame = self.frames.peek()
        inputs = InstructorInputs(
            instruction=instruction,
            locals=frame.locals,
            op_stack=frame.op_stack,
            constants=frame.jvm_class.constants,
            loader=self.class_loader
        )
        self._echo(f'op_stack: {frame.op_stack._values}')
        self._echo(f'{frame.jvm_class.name}#{frame.method_name}{frame.method_descriptor}, {instruction}')
        actions = execute_instruction(inputs)
        for action in actions:
            self._echo('  ' + str(action))
            self.act(action)

        self._echo('')

    def act(self, action):
        """Execute `action`

        The action's type name will be translated to snake case and prefixed with an underscore.
        The method with the snake cased name will be called using the action.
        For example:
         - The action `IncrementProgramCounter()` will be converted to the name '_increment_program_counter'
         - The call will be `self._increment_program_counter(action)`
        """
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
        """Push a new class instance on to the current frame's op stack

        There is no need to call the `<init>` constructor (or determine which one to call).
        The compiler should follow this action with the appropriate call.
        So we will only need to initialize the instance fields to their default values according to type.
        """
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
        """Invoke a method

        The structure of Machine makes this simple.
        We just create a frame for the method and push it onto the frame stack.
        The next time the Machine fetches an instruction to execute
        it will find the first instruction of the new method.

        Don't forget to populate the frame's Locals array with the parameters.
        """
        class_name = action.class_name
        method_key = action.method_key

        loader = self.class_loader
        class_ = loader.get_the_class(class_name)
        method = loader.resolve_method(class_name, method_key)

        if method.is_native:
            raise NativeNotSupported(
                f'Cannot invoke method {class_.name}#{method.name} because native methods are not supported'
            )

        frame = Frame.from_class_and_method(class_, method)
        self.frames.push(frame)

        if len(method.instructions) < 1:
            self._return_void(None)
        else:
            for index, value in enumerate(action.arguments):
                frame.locals.store(index, value)

    # noinspection PyUnusedLocal
    def _return_void(self, action):
        """Return from the current frame without a value and increment the program counter"""
        self.frames.pop()
        self._increment_program_counter(None)

    def _return_result(self, action):
        """Return from the current frame with a value and increment the program counter

        This is achieved like this:
         - Take the value from the current frame's op stack
         - Pop the frame stack. Now the current frame has changed
         - Push the value onto the new current frame's op stack
         - Increment the program counter
        """
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
        """Throw an exception instance

        We do this recursively:
        If the current frame has a relevant handler we jump to its handler_pc.
        If not we pop the current frame, and repeat the process for the new current frame using a recursive call.
        If there are no more frames to pop this exception is unhandled and execution should stop.
        """
        frames = self.frames
        frame = frames.peek()
        handlers = frame.exception_handlers.find_handlers(frame.pc)
        for handler in handlers:
            class_name = handler.catch_type
            type_match = is_value_instance_of(instance, class_as_descriptor(class_name), self.class_loader)
            if type_match:
                stack = frame.op_stack
                stack.clear()
                stack.push(instance)
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
        """Perform class loading operations

        When a class is accessed for the first time we need to:
         - Initialize the static fields to their default values
         - Call the `<clinit>` method for the class
        """
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

    def _echo(self, text):
        depth = self.frames.size()
        prefix = '|  ' * depth
        self.echo(prefix + str(text))


def _to_snake_case(text):
    new_letters = [c if c.islower() else '_' + c.lower() for c in text]
    return ''.join(new_letters)


# noinspection PyUnusedLocal
def _default_echo(*args, **kwargs):
    pass


def run(loader, main_class_name, echo=None):
    """Run the class named `main_class_name` using `loader`

    :param loader: ClassLoader, the loader to use
    :param main_class_name: str, the name of the main class
    :param echo: a print-like method that, if provided, will be used for tracing execution
    """
    class_ = loader.get_the_class(main_class_name)
    # noinspection SpellCheckingInspection
    key = MethodKey('main', '([Ljava/lang/String;)V')
    method = class_.methods[key]
    frame = Frame.from_class_and_method(class_, method)
    machine = Machine(loader, echo=echo)
    machine.frames.push(frame)
    machine.run()
