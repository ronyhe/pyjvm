from pyjvm.core import actions
from pyjvm.core.actions import IncrementProgramCounter, Actions
from pyjvm.core.hierarchies import is_value_instance_of
from pyjvm.core.jvm_types import Integer, ArrayReferenceType, ObjectReferenceType
from pyjvm.instructions.instructions import bytecode, Instructor
from pyjvm.utils import value_array_type_indicators
from pyjvm.utils.utils import class_as_descriptor, field_name_from_field_ref


@bytecode('instanceof')
class InstanceOf(Instructor):
    """Pushes Integer value 1 if top-of-stack is an instance of the provided class, else, pushes Integer value 0"""

    def execute(self):
        constant_index = self.operand_as_int()
        constant = self.constants[constant_index]
        class_name = constant.name.value

        obj = self.peek_op_stack()
        if obj.is_null:
            answer = False
        else:
            answer = is_value_instance_of(obj, class_as_descriptor(class_name), self.loader)

        if answer:
            result = Integer.create_instance(1)
        else:
            result = Integer.create_instance(0)

        return IncrementProgramCounter.after(
            actions.Pop(),
            actions.Push(result)
        )


@bytecode('checkcast')
class CheckCast(Instructor):
    """Throws CheckCastException if top-of-stack is not an instance of the provided class"""

    def execute(self):
        constant_index = self.operand_as_int()
        constant = self.constants[constant_index]
        class_name = constant.name.value

        obj = self.peek_op_stack()
        answer = obj.is_null or is_value_instance_of(obj, class_as_descriptor(class_name), self.loader)
        if answer:
            return IncrementProgramCounter()
        else:
            return actions.throw_check_cast()


@bytecode('arraylength')
class ArrayLength(Instructor):
    """Returns an Integer value representing the length of the array at top-of-stack"""

    def execute(self):
        array = self.peek_op_stack()
        if array.is_null:
            return actions.throw_null_pointer()
        else:
            size = len(array.value)
            result = Integer.create_instance(size)

            return IncrementProgramCounter.after(
                actions.Pop(),
                actions.Push(result)
            )


class CreateNewArray(Instructor):
    """Creates a new array and pushes it onto the stack

    The size of the array is popped of the stack.
    The type of the array is found via the abstract method `_get_type'.
    The array is populated with instances of the default value for the type.
    """

    def execute(self):
        type_ = self._get_type()
        size = self.peek_op_stack().value
        if size < 0:
            return actions.throw_negative_array_size()
        else:
            elements = [type_.create_instance(type_.default_value) for _ in range(size)]
            result = ArrayReferenceType(type_).create_instance(elements)
            return IncrementProgramCounter.after(
                actions.Pop(),
                actions.Push(result)
            )

    def _get_type(self):
        raise NotImplementedError()


@bytecode('newarray')
class NewValueArray(CreateNewArray):
    """Creates a new array of primitive type

    The type is provided in the instruction as number.
    See ../utils/value_array_type_indicators.py for more information
    """

    def _get_type(self):
        type_indicator = self.operand_as_int()
        type_ = value_array_type_indicators.type_by_indicator(type_indicator)
        return type_


@bytecode('anewarray')
class NewRefArray(CreateNewArray):
    """Creates a new array of reference type instances"""

    def _get_type(self):
        index = self.operand_as_int()
        const = self.constants[index]
        class_name = const.name.value
        type_ = ObjectReferenceType(refers_to=class_name)
        return type_


@bytecode('multianewarray')
class NewMultiArray(Instructor):
    """Creates a new multidimensional array

    The amount of dimensions is provided in the instruction operands.
    The size of each dimension is popped off the stack
    """

    def execute(self):
        class_ = self.operand_as_constant()
        class_name = class_.name.value
        base_type = ObjectReferenceType(class_name)

        num_dimensions = self.operand_as_int(index=1)
        dimensions = [v.value for v in self.peek_many(num_dimensions)]
        if any(d < 0 for d in dimensions):
            return actions.throw_negative_array_size()

        array_type = base_type
        for _ in range(num_dimensions):
            array_type = ArrayReferenceType(array_type)

        array_value = create_levels(dimensions, lambda: base_type.create_instance(base_type.default_value))

        return IncrementProgramCounter.after(
            actions.Pop(num_dimensions),
            actions.Push(array_type.create_instance(array_value))
        )


@bytecode('athrow')
class Throw(Instructor):
    """Pop an exception off the stack and throw it"""

    def execute(self):
        obj = self.peek_op_stack()
        if obj.is_null:
            action = actions.throw_null_pointer()
        else:
            action = actions.ThrowObject(obj)

        return Actions(
            action
        )


@bytecode('new')
class New(Instructor):
    """Push a new instance of the provided class onto the stack"""

    def execute(self):
        class_constant_index = self.operand_as_int()
        class_constant = self.constants[class_constant_index]
        class_name = class_constant.name.value
        class_ = self.loader.get_the_class(class_name)
        return IncrementProgramCounter.after(
            actions.PushNewInstance(class_)
        )


@bytecode('getfield')
class GetField(Instructor):
    """Push the value that is currently stored in a field

    The field is resolved by taking an index into the constant pool from the instruction operands.
    """

    def execute(self):
        field_ref = self.operand_as_constant()
        name = field_name_from_field_ref(field_ref)
        obj = self.peek_op_stack()
        if obj.is_null:
            return actions.throw_null_pointer()

        value = obj.value.fields[name]
        return IncrementProgramCounter.after(
            actions.Pop(),
            actions.Push(value)
        )


@bytecode('putfield')
class PutField(Instructor):
    """Pop stack and store value in field

    The field is resolved by taking an index into the constant pool from the instruction operands.
    """

    def execute(self):
        field_ref = self.operand_as_constant()
        name = field_name_from_field_ref(field_ref)
        value = self.peek_op_stack(0)
        obj = self.peek_op_stack(1)

        if obj.is_null:
            return actions.throw_null_pointer()

        return IncrementProgramCounter.after(
            actions.Pop(2),
            actions.PutField(obj, name, value)
        )


@bytecode('putstatic')
class PutStatic(Instructor):
    """Pop stack and store value in static field

    The field is resolved by taking an index into the constant pool from the instruction operands.
    """

    def execute(self):
        field_ref = self.operand_as_constant()
        field_name = field_name_from_field_ref(field_ref)
        class_name = field_ref.class_.name.value
        value = self.peek_op_stack()
        return IncrementProgramCounter.after(
            actions.Pop(),
            actions.PutStatic(class_name, field_name, value)
        )


@bytecode('getstatic')
class GetStatic(Instructor):
    """Push the value that is currently stored in a static field

    The field is resolved by taking an index into the constant pool from the instruction operands.
    """

    def execute(self):
        field_ref = self.operand_as_constant()
        field_name = field_name_from_field_ref(field_ref)
        class_name = field_ref.class_.name.value

        value = self.loader.get_the_statics(class_name)[field_name]
        return IncrementProgramCounter.after(
            actions.Push(value)
        )


def create_levels(levels, base_factory):
    """Create a multidimensional array

    :param levels: An Iterable if ints representing the size of each level
    :param base_factory: A nullary function that returns a new instance of the basic unit of the array
    :return: Nested lists
    """

    def loop(current, rest):
        if len(rest) == 0:
            return [base_factory() for _ in range(current)]
        else:
            return [loop(rest[0], rest[1:]) for _ in range(current)]

    return loop(levels[0], levels[1:])
