from pyjvm import value_array_type_indicators
from pyjvm.instructions.instructions import Instructor, bytecode

from pyjvm.jvm_types import ArrayReferenceType, ObjectReferenceType, Integer


# noinspection PyAbstractClass
class _ReferenceInstructor(Instructor):
    def first_op_as_int(self):
        return int(self.instruction.operands[0].value)

    def constant_from_index(self):
        index = self.first_op_as_int()
        return self.machine.current_constants()[index]


def _as_boolean_value(bool_):
    if bool_:
        num = 1
    else:
        num = 0
    instance = Integer.create_instance(num)
    return instance


@bytecode('putstatic')
class PutStatic(_ReferenceInstructor):
    def execute(self):
        field_ref = self.constant_from_index()
        class_name = field_ref.class_.name.value
        field_name = field_ref.name_and_type.name.value
        value = self.machine.current_op_stack().pop()
        self.machine.put_static_field(class_name, field_name, value)


@bytecode('getstatic')
class GetStatic(_ReferenceInstructor):
    def execute(self):
        field_ref = self.constant_from_index()
        class_name = field_ref.class_.name.value
        field_name = field_ref.name_and_type.name.value
        value = self.machine.get_static_field(class_name, field_name)
        self.machine.current_op_stack().push(value)


@bytecode('new')
class New(_ReferenceInstructor):
    def execute(self):
        class_ref = self.constant_from_index()
        class_name = class_ref.name.value
        value = self.machine.create_new_class_instance(class_name)
        self.machine.current_op_stack().push(value)


@bytecode('putfield')
class PutField(_ReferenceInstructor):
    def execute(self):
        field_ref = self.constant_from_index()
        field_name = field_ref.name_and_type.name.value

        stack = self.machine.current_op_stack()
        value = stack.pop()
        instance = stack.pop()

        instance.value.fields[field_name] = value


@bytecode('getfield')
class GetField(_ReferenceInstructor):
    def execute(self):
        field_ref = self.constant_from_index()
        field_name = field_ref.name_and_type.name.value
        stack = self.machine.current_op_stack()
        instance = stack.pop()
        value = instance.value.fields[field_name]
        stack.push(value)


@bytecode('newarray')
class NewValueArray(_ReferenceInstructor):
    def execute(self):
        indicator = self.first_op_as_int()
        element_type = value_array_type_indicators.type_by_indicator(indicator)

        stack = self.machine.current_op_stack()
        length = stack.pop().value
        elements = [element_type.create_instance(element_type.default_value) for _ in range(length)]

        array_type = ArrayReferenceType(element_type)
        value = array_type.create_instance(elements)
        stack.push(value)


@bytecode('anewarray')
class NewReferenceArray(_ReferenceInstructor):
    def execute(self):
        stack = self.machine.current_op_stack()
        length = int(stack.pop().value)
        class_name = self.constant_from_index().name.value
        element_type = ObjectReferenceType(class_name)
        elements = [element_type.create_instance(element_type.default_value) for _ in range(length)]
        array_type = ArrayReferenceType(element_type)
        array = array_type.create_instance(elements)
        stack.push(array)


@bytecode('arraylength')
class ArrayLength(Instructor):
    def execute(self):
        stack = self.machine.current_op_stack()
        array = stack.pop()
        value = Integer.create_instance(len(array.value))
        stack.push(value)


@bytecode('instanceof')
class InstanceOf(_ReferenceInstructor):
    def execute(self):
        stack = self.machine.current_op_stack()
        descriptor = self.constant_from_index().value
        obj = stack.pop()
        is_instance = (not obj.is_null) and self.machine.is_reference_an_instance_of(obj, descriptor)
        stack.push(_as_boolean_value(is_instance))
