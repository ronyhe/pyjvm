from typing import Iterable

from jawa.constants import ConstantPool
from jawa.util.bytecode import Instruction

from pyjvm.class_loaders import ClassLoader
from pyjvm.frame_locals import Locals
from pyjvm.hierarchies import is_value_instance_of
from pyjvm.instructions.instructions import execute_instruction
from pyjvm.jvm_class import BytecodeMethod, JvmClass, JvmObject, NAME_OF_STATIC_CONSTRUCTOR
from pyjvm.jvm_types import JvmValue, ObjectReferenceType
from pyjvm.stack import Stack


class Frame:
    @classmethod
    def from_class_and_method(cls, class_: JvmClass, method: BytecodeMethod):
        return cls(
            class_,
            Locals(method.max_locals),
            Stack(max_depth=method.max_stack),
            method.instructions
        )

    def __init__(self,
                 class_: JvmClass,
                 _locals: Locals,
                 op_stack: Stack[JvmValue],
                 instructions: Iterable[Instruction]):
        self.class_ = class_
        self.locals = _locals
        self.op_stack = op_stack
        self.instructions = tuple(instructions)

    def execute(self, machine):
        pc = 0
        instruction = self.next_instruction(pc)
        while instruction is not None:
            execute_instruction(instruction, machine)
            pc += 1
            instruction = self.next_instruction(pc)

    def next_instruction(self, pc):
        for ins in self.instructions:
            if ins.pos >= pc:
                return ins

        return None


class Machine:
    def __init__(self, class_loader: ClassLoader):
        self.current_frame: Frame = None
        self.class_loader = class_loader
        self.class_loader.first_load_function = self.run_class_init

    def run_frame(self, frame: Frame):
        self.current_frame = frame
        frame.execute(self)

    def current_locals(self) -> Locals:
        return self.current_frame.locals

    def current_op_stack(self) -> Stack[JvmValue]:
        return self.current_frame.op_stack

    def current_constants(self) -> ConstantPool:
        return self.current_frame.class_.constants

    def get_static_field(self, class_name, field_name):
        return self.class_loader.get_the_statics(class_name)[field_name]

    def put_static_field(self, class_name, field_name, value):
        self.class_loader.get_the_statics(class_name)[field_name] = value

    def create_new_class_instance(self, class_name):
        fields = self.collect_fields(class_name)
        obj = ObjectReferenceType(class_name).create_instance(JvmObject.defaults(fields))
        return obj

    def collect_fields(self, class_name):
        return self.class_loader.collect_fields_in_ancestors(class_name)

    def run_class_init(self, the_class):
        try:
            method = the_class.methods[NAME_OF_STATIC_CONSTRUCTOR]
        except KeyError:
            return

        self.run_frame(Frame.from_class_and_method(the_class, method))

    def is_reference_an_instance_of(self, reference: JvmValue, descriptor: str) -> bool:
        return is_value_instance_of(reference, descriptor, self.class_loader)
