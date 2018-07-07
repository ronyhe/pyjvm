from jawa.cf import ClassFile
from jawa.constants import ConstantPool
from jawa.util.bytecode import Instruction

from pyjvm.class_loaders import FixedClassLoader, EmptyClassLoader
from pyjvm.frame_locals import Locals
from pyjvm.jawa_conversions import convert_class_file
from pyjvm.jvm_class import JvmClass
from pyjvm.jvm_types import ObjectReferenceType
from pyjvm.machine import Frame, Machine
from pyjvm.stack import Stack


class BlankTestMachine(Machine):
    def __init__(self, class_loader=None):
        if class_loader is None:
            class_loader = EmptyClassLoader()
        super().__init__(class_loader)
        self.current_frame = Frame(JvmClass('SomeClass', 'SomeBase', ConstantPool()), Locals(5), Stack(), [])

    def step_instruction(self, *args):
        if len(args) == 1 and isinstance(args[0], Instruction):
            inst = args[0]
        else:
            inst = Instruction.create(*args)

        # noinspection PyProtectedMember
        inst = inst._replace(pos=0)
        self.current_frame.instructions = tuple([inst])
        self.run_frame(self.current_frame)


class _DummyClass:
    DESCRIPTOR = 'I'

    def __init__(self):
        self.name = 'ClassName'
        self.class_file = ClassFile.create(self.name)
        self.instance_field = self.class_file.fields.create('instance_field', self.DESCRIPTOR)
        self.class_field = self.class_file.fields.create('class_field', self.DESCRIPTOR)
        self.class_field.access_flags.set('acc_static', True)
        self.type = ObjectReferenceType(self.name)

    def create_field_ref(self, constants, field):
        return constants.create_field_ref(self.name, field.name, self.DESCRIPTOR)

    def instance_field_ref(self, constants):
        return self.create_field_ref(constants, self.instance_field)

    def class_field_ref(self, constants):
        return self.create_field_ref(constants, self.class_field)


DUMMY_SUB_CLASS_NAME = 'Sub'
DUMMY_CLASS = _DummyClass()


def dummy_loader():
    return FixedClassLoader({
        DUMMY_CLASS.name: convert_class_file(DUMMY_CLASS.class_file),
        DUMMY_SUB_CLASS_NAME: convert_class_file(ClassFile.create(DUMMY_SUB_CLASS_NAME, DUMMY_CLASS.name))
    })
