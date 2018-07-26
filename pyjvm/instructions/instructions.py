"""
This module implements a dispatch mechanism to execute JVM instructions.
It also defines several tools that are used across instructions.

At a high level, it provides a registry for `Instructor` instances, and several utility functions for subscribing to it.
When `execute_instruction` is called, it dispatches it to the correct Instructor via the registry and returns the
resulting `Actions`

`bytecode`, `bytecode_dict` and `bytecode_list` are meant to be used as decorators for sub classes of `Instructor`.
    .. code::

        @bytecode('iload')
        class ILoadImplementation(Instructor):
            pass

They leverage the `decorator` method of `ClassRegistry`, so refer to that class for more information.

"""
from collections import OrderedDict

from pyjvm.actions import IncrementProgramCounter, Action, Actions
from pyjvm.utils.class_registry import ClassRegistry

_registry = ClassRegistry()

bytecode = _registry.decorator


def bytecode_dict(names_and_args):
    """A decorator that enables defining instructions and their corresponding arguments

    For example, this code:
        .. code::

            @bytecode_dict({
                'iload_0': [0],
                'iload_1': [1]
            })
            class SomeInstructor(Instructor):
                pass

    Is equivalent to this code:
        .. code::

            @bytecode('iload_0', 0)
            @bytecode('iload_1', 1)
            class SomeInstructor(Instructor):
                pass

    """
    dic = OrderedDict(names_and_args)

    def func(class_):
        for name, args in dic.items():
            class_ = bytecode(name, *args)(class_)

        return class_

    return func


def bytecode_list(names):
    """A decorator that enables defining several instructions for the same Instructor

    For example, this code:
        .. code::

            @bytecode_list(['sipush', 'bipush'])
            class SomeInstructor(Instructor):
                pass

    Is equivalent to this code:
        .. code::

            @bytecode('sipush')
            @bytecode('bipush')
            class SomeInstructor(Instructor):
                pass
    """
    return bytecode_dict({name: [] for name in names})


class InstructorInputs:
    """The inputs that a basic Instructor expects.

    Sub classes can receive other arguments using the usual method mechanisms
    """

    # noinspection PyShadowingBuiltins
    def __init__(self, *, instruction, locals, op_stack, constants, loader):
        self.instruction = instruction
        self.locals = locals
        self.op_stack = op_stack
        self.constants = constants
        self.loader = loader


class Instructor:
    """An abstract class that translates an `Instruction` into `Actions`"""

    def __init__(self, inputs):
        self.instruction = inputs.instruction
        self.locals = inputs.locals
        self.op_stack = inputs.op_stack
        self.constants = inputs.constants
        self.loader = inputs.loader

    def execute(self):
        """Emit `Actions` or an `Action` that correspond to the `instruction`"""
        raise NotImplementedError()

    def operand_as_int(self, index=0):
        """Return an `int` value from the literal `operand` at `index`"""
        return int(self.instruction.operands[index].value)

    def operand_as_constant(self, index=0):
        """Return a constant using the operand at `index` as an index into the `self.constants`"""
        const_index = self.operand_as_int(index)
        return self.constants[const_index]

    def peek_op_stack(self, *args, **kwargs):
        """Return top-of-stack"""
        return self.op_stack.peek(*args, **kwargs)

    def peek_many(self, amount):
        """Return the `amount` first objects on the stack"""
        return [self.peek_op_stack(i) for i in range(amount)]


def execute_instruction(inputs):
    """Return `Actions` that simulate the execution of `inputs.instruction`"""
    instruction_name = inputs.instruction.mnemonic
    executor = _registry.get(instruction_name, inputs)
    action_or_actions = executor.execute()
    if isinstance(action_or_actions, Action):
        return Actions(action_or_actions)
    else:
        return action_or_actions


def get_implemented_instructions():
    """Return the names of the instructions that were registered"""
    return _registry.keys()


@bytecode_list([
    'nop',
    'monitorenter',
    'monitorexit',
    'breakpoint',
    'impdep1',
    'impdep2'
])
class NoOp(Instructor):
    """Do nothing when executing these instructions"""

    def execute(self):
        return IncrementProgramCounter()


@bytecode_list([
    'jsr',
    'jsr_w',
    'ret',
    'invokedynamic',
    'wide'
])
class InstructionNotImplemented(Instructor):
    """Raise an error when encountering these instructions"""

    def execute(self):
        name = self.instruction.mnemonic
        raise NotImplementedError(f'The {name} instruction is not implemented by this jvm')

# Uh-Oh, we broke a rule.
# The `Instructor` sub classes use elements defined in this module.
# So they have to be imported after those definitions.
# However, when a user imports this module, they expect the `execute_instruction` to actually work.
# That's why we import the instruction modules here and not, as is convention, at the top.

# noinspection PyUnresolvedReferences
from pyjvm.instructions import loads_and_stores
# noinspection PyUnresolvedReferences
from pyjvm.instructions import stack_instructions
# noinspection PyUnresolvedReferences
from pyjvm.instructions import constant_instructions
# noinspection PyUnresolvedReferences
from pyjvm.instructions import conversions
# noinspection PyUnresolvedReferences
from pyjvm.instructions import math
# noinspection PyUnresolvedReferences
from pyjvm.instructions import references
# noinspection PyUnresolvedReferences
from pyjvm.instructions import invocations
# noinspection PyUnresolvedReferences
from pyjvm.instructions import control
# noinspection PyUnresolvedReferences
from pyjvm.instructions import comparisons
