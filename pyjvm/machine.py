from typing import Iterable, Set

from jawa.constants import ConstantPool
from jawa.util.bytecode import Instruction
from jawa.util.descriptor import field_descriptor

from pyjvm.class_loaders import ClassLoader
from pyjvm.frame_locals import Locals
from pyjvm.instructions.instructions import execute_instruction
from pyjvm.jawa_conversions import convert_type
from pyjvm.jvm_class import BytecodeMethod, JvmClass, JvmObject
from pyjvm.jvm_types import JvmValue, ObjectReferenceType, RootObjectType
from pyjvm.stack import Stack


class Frame:
    @classmethod
    def from_class_and_method(cls, class_: JvmClass, method: BytecodeMethod):
        return cls(
            class_,
            Locals(method.max_locals),
            Stack(max_depth=method.max_stack),
            method.instructions,
            0
        )

    def __init__(self,
                 class_: JvmClass,
                 _locals: Locals,
                 op_stack: Stack[JvmValue],
                 instructions: Iterable[Instruction],
                 position: int):
        self.class_ = class_
        self.locals = _locals
        self.op_stack = op_stack
        self.instructions = tuple(instructions)
        self.position = position

    def next_instruction(self):
        for ins in self.instructions:
            if ins.pos >= self.position:
                return ins

        return None


class Machine:
    @classmethod
    def from_class_and_method(cls, the_class: JvmClass, method: BytecodeMethod):
        frame = Frame.from_class_and_method(the_class, method)
        frames = Stack()
        frames.push(frame)
        instruction = frame.next_instruction()
        return cls(frames, instruction, ClassLoader())

    def __init__(self,
                 frames: Stack[Frame],
                 instruction: Instruction,
                 class_loader: ClassLoader):
        self.frames = frames
        self.instruction = instruction
        self.class_loader = class_loader
        self.statics = dict()

    def step(self):
        execute_instruction(self.instruction, self)
        frame = self.current_frame()
        frame.position += 1
        self.instruction = frame.next_instruction()

    def run_frame(self):
        while self.instruction is not None:
            self.step()

    def push_frame(self, frame):
        self.frames.push(frame)
        self.instruction = frame.next_instruction()

    def current_frame(self) -> Frame:
        return self.frames.peek()

    def current_locals(self) -> Locals:
        return self.current_frame().locals

    def current_op_stack(self) -> Stack[JvmValue]:
        return self.current_frame().op_stack

    def current_constants(self) -> ConstantPool:
        return self.current_frame().class_.constants

    def get_static_field(self, class_name, field_name):
        self.load_class_if_needed(class_name)
        return self.statics[class_name][field_name]

    def put_static_field(self, class_name, field_name, value):
        self.load_class_if_needed(class_name)
        self.statics[class_name][field_name] = value

    def load_class_if_needed(self, class_name):
        if class_name not in self.statics.keys():
            self.load_class(class_name)

    def load_class(self, class_name):
        the_class = self.class_loader.get_by_name(class_name)
        field_dict = {name: type_.create_instance(type_.default_value) for name, type_ in
                      the_class.static_fields.items()}
        self.statics[class_name] = field_dict
        self.run_class_init(the_class)

    def create_new_class_instance(self, class_name):
        fields = self.load_if_needed_and_collect_fields(class_name)
        obj = ObjectReferenceType(class_name).create_instance(JvmObject.defaults(fields))
        return obj

    def load_if_needed_and_collect_fields(self, class_name):
        acc = dict()
        name = class_name
        while not name == RootObjectType.refers_to:
            self.load_class_if_needed(name)
            the_class = self.class_loader.get_by_name(name)
            acc.update(the_class.fields)
            name = the_class.name_of_base

        return acc

    def run_class_init(self, the_class):
        try:
            method = the_class.methods['clinit']
        except KeyError:
            return

        self.push_frame(Frame.from_class_and_method(the_class, method))
        self.run_frame()

    def is_reference_an_instance_of(self, reference: JvmValue, descriptor: str) -> bool:
        type_, value = reference.type, reference.value
        if reference.is_null:
            raise ValueError('Cannot instance_of check null value')
        if type_.is_value:
            raise ValueError('Cannot instance_of check value types. Only references')
        descriptor_type = convert_type(field_descriptor(descriptor))
        if not descriptor_type.is_reference:
            return False
        if type_.is_array_reference and descriptor_type.is_array_reference:
            return _is_array_ref_an_instance_of(type_, descriptor_type)
        elif type_.is_class_reference and descriptor_type.is_class_reference:
            self.load_class_if_needed(type_.refers_to)
            type_class = self.class_loader.get_by_name(type_.refers_to)
            roots = [type_.refers_to] + list(type_class.interfaces)
            return any(descriptor_type.refers_to in self._get_ancestors(root) for root in roots)
        else:
            raise ValueError('Unexpected execution path')

    def _get_ancestors(self, name: str) -> Set[str]:
        acc = set()
        acc.add(name)
        curr = name
        while not curr == RootObjectType.refers_to:
            self.load_class_if_needed(curr)
            the_class = self.class_loader.get_by_name(curr)
            next_name = the_class.name_of_base
            acc.add(next_name)
            curr = next_name

        return acc
