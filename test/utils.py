from jawa.constants import ConstantPool
from jawa.util.bytecode import Instruction

from pyjvm.actions import IncrementProgramCounter
from pyjvm.frame_locals import Locals
from pyjvm.instructions.instructions import InstructorInputs, execute_instruction
from pyjvm.jvm_types import Integer
from pyjvm.stack import Stack

SOME_INT = Integer.create_instance(2)

_OP_STACK_KEY = 'op_stack'
_INSTRUCTION_KEY = 'instruction'


class DefaultInputs(InstructorInputs):
    DEFAULTS = {
        'locals': lambda: Locals(5),
        _OP_STACK_KEY: lambda: Stack(),
        'constants': lambda: ConstantPool
    }

    def __init__(self, **kwargs):
        actual_args = dict()
        actual_args.update(kwargs)
        for key, default_factory in self.DEFAULTS.items():
            try:
                v = actual_args[key]
            except KeyError:
                v = default_factory()

            actual_args[key] = v

        # op_stack can be provided as iterable, coerce it to a Stack
        stack_elements = actual_args[_OP_STACK_KEY]
        actual_args[_OP_STACK_KEY] = Stack(values=list(stack_elements))

        super().__init__(**actual_args)


def assert_instruction(expected=None, **kwargs):
    if expected is None:
        expected = []
    args = dict(kwargs)

    # instruction can be a string, coerce it to an instruction if needed
    instruction = args[_INSTRUCTION_KEY]
    if isinstance(instruction, str):
        instruction = Instruction.create(instruction)
    args[_INSTRUCTION_KEY] = instruction

    inputs = DefaultInputs(**args)
    actions = execute_instruction(inputs)
    assert actions.has(*expected)


def assert_incrementing_instruction(expected=None, **kwargs):
    if expected is None:
        expected = []
    expected.append(IncrementProgramCounter)
    assert_instruction(expected=expected, **kwargs)
