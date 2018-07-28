from jawa.constants import ConstantPool
from jawa.util.bytecode import Instruction

from pyjvm.actions import IncrementProgramCounter
from pyjvm.instructions.instructions import InstructorInputs, execute_instruction
from pyjvm.model.class_loaders import FixedClassLoader
from pyjvm.model.frame_locals import Locals
from pyjvm.model.jvm_types import Integer
from pyjvm.model.stack import Stack
from pyjvm.utils.utils import literal_operand, constant_operand

SOME_INT = Integer.create_instance(2)

_OP_STACK_KEY = 'op_stack'
_INSTRUCTION_KEY = 'instruction'

NON_EMPTY_INSTRUCTION_LIST = [Instruction.create('nop')]

NPE_CLASS_NAME = 'java/lang/NullPointerException'
CHECK_CAST_CLASS_NAME = 'java/lang/CheckCastException'

    
def dummy_loader():
    return FixedClassLoader({})


class DefaultInputs(InstructorInputs):
    DEFAULTS = {
        'locals': lambda: Locals(5),
        _OP_STACK_KEY: Stack,
        'constants': ConstantPool,
        'loader': dummy_loader
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


def constant_instruction(name, constant):
    return Instruction.create(name, [constant_operand(constant)])


def literal_instruction(name, literal):
    return Instruction.create(name, [literal_operand(literal)])
