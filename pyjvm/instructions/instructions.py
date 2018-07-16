from collections import OrderedDict

from pyjvm.actions import IncrementProgramCounter, Action, Actions
from pyjvm.class_registry import ClassRegistry

_registry = ClassRegistry()

bytecode = _registry.decorator


def bytecode_dict(names_and_args):
    dic = OrderedDict(names_and_args)

    def func(class_):
        for name, args in dic.items():
            class_ = bytecode(name, *args)(class_)

        return class_

    return func


def bytecode_list(names):
    return bytecode_dict({name: [] for name in names})


class InstructorInputs:
    # noinspection PyShadowingBuiltins
    def __init__(self, *, instruction, locals, op_stack, constants, loader):
        self.instruction = instruction
        self.locals = locals
        self.op_stack = op_stack
        self.constants = constants
        self.loader = loader


class Instructor:
    def __init__(self, inputs):
        self.instruction = inputs.instruction
        self.locals = inputs.locals
        self.op_stack = inputs.op_stack
        self.constants = inputs.constants
        self.loader = inputs.loader

    def execute(self):
        raise NotImplementedError()

    def operand_as_int(self, index=0):
        return int(self.instruction.operands[index].value)

    def operand_as_constant(self, index=0):
        index = self.operand_as_int(index)
        return self.constants[index]

    def peek_op_stack(self, *args, **kwargs):
        return self.op_stack.peek(*args, **kwargs)

    def peek_many(self, amount):
        for i in range(amount):
            yield self.peek_op_stack(i)


def execute_instruction(inputs):
    instruction_name = inputs.instruction.mnemonic
    executor = _registry.get(instruction_name, inputs)
    action_or_actions = executor.execute()
    if isinstance(action_or_actions, Action):
        return Actions(action_or_actions)
    else:
        return action_or_actions


def get_implemented_instructions():
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
    def execute(self):
        return IncrementProgramCounter()


@bytecode_list([
    'jsr',
    'jsr_w',
    'ret',
    'invokedynamic'
])
class InstructionNotImplemented(Instructor):
    def execute(self):
        name = self.instruction.mnemonic
        raise NotImplementedError(f'The {name} instruction is not implemented by this jvm')


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
