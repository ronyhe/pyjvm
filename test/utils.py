from jawa.cf import ClassFile
from jawa.constants import ConstantPool
from jawa.util.bytecode import Instruction, Operand, OperandTypes

from pyjvm.actions import IncrementProgramCounter
from pyjvm.class_loaders import FixedClassLoader
from pyjvm.frame_locals import Locals
from pyjvm.instructions.instructions import InstructorInputs, execute_instruction
from pyjvm.jawa_conversions import convert_class_file
from pyjvm.jvm_types import Integer, ObjectReferenceType
from pyjvm.stack import Stack

SOME_INT = Integer.create_instance(2)

_OP_STACK_KEY = 'op_stack'
_INSTRUCTION_KEY = 'instruction'


class _DummyClass:
    DESCRIPTOR = 'I'

    def __init__(self):
        self.name = 'ClassName'
        self.class_file = ClassFile.create(self.name)
        self.instance_field = self.class_file.fields.create('instance_field', self.DESCRIPTOR)
        self.class_field = self.class_file.fields.create('class_field', self.DESCRIPTOR)
        self.class_field.access_flags.set('acc_static', True)
        self.type = ObjectReferenceType(self.name)
        self.method = self.class_file.methods.create('some_method', '(I)I', code=True)
        self.method.code.assemble([])

    def create_field_ref(self, constants, field):
        return constants.create_field_ref(self.name, field.name, self.DESCRIPTOR)

    def instance_field_ref(self, constants):
        return self.create_field_ref(constants, self.instance_field)

    def class_field_ref(self, constants):
        return self.create_field_ref(constants, self.class_field)

    def method_ref(self, constants):
        return constants.create_method_ref(
            DUMMY_CLASS.name,
            self.method.name.value,
            DUMMY_CLASS.method.descriptor.value
        )


DUMMY_SUB_CLASS_NAME = 'Sub'
DUMMY_CLASS = _DummyClass()


def dummy_loader():
    return FixedClassLoader({
        DUMMY_CLASS.name: convert_class_file(DUMMY_CLASS.class_file),
        DUMMY_SUB_CLASS_NAME: convert_class_file(ClassFile.create(DUMMY_SUB_CLASS_NAME, DUMMY_CLASS.name))
    })


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
    return Instruction.create(name, [Operand(OperandTypes.CONSTANT_INDEX, constant.index)])


def literal_instruction(name, literal):
    return Instruction.create(name, [Operand(OperandTypes.LITERAL, literal)])
