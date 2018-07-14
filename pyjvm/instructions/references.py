from pyjvm import actions, value_array_type_indicators
from pyjvm.actions import IncrementProgramCounter, Actions, ThrowCheckCastException
from pyjvm.hierarchies import is_value_instance_of
from pyjvm.instructions.instructions import bytecode, Instructor
from pyjvm.jvm_types import Integer, ArrayReferenceType, ObjectReferenceType
from pyjvm.utils import class_as_descriptor


@bytecode('instanceof')
class InstanceOf(Instructor):
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
            actions.Push(result)
        )


@bytecode('checkcast')
class CheckCast(Instructor):
    def execute(self):
        constant_index = self.operand_as_int()
        constant = self.constants[constant_index]
        class_name = constant.name.value

        obj = self.peek_op_stack()
        answer = obj.is_null or is_value_instance_of(obj, class_as_descriptor(class_name), self.loader)
        if answer:
            return Actions(
                IncrementProgramCounter()
            )
        else:
            return Actions(
                ThrowCheckCastException()
            )


@bytecode('arraylength')
class ArrayLength(Instructor):
    def execute(self):
        array = self.peek_op_stack()
        if array.is_null:
            return Actions(
                actions.ThrowNullPointerException()
            )
        else:
            size = len(array.value)
            result = Integer.create_instance(size)

            return IncrementProgramCounter.after(
                actions.Pop(),
                actions.Push(result)
            )


class CreateNewArray(Instructor):
    def execute(self):
        type_ = self._get_type()
        size = self.peek_op_stack().value
        if size < 0:
            return Actions(
                actions.ThrowNegativeArraySizeException()
            )
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
    def _get_type(self):
        type_indicator = self.operand_as_int()
        type_ = value_array_type_indicators.type_by_indicator(type_indicator)
        return type_


@bytecode('anewarray')
class NewValueArray(CreateNewArray):
    def _get_type(self):
        index = self.operand_as_int()
        const = self.constants[index]
        class_name = const.name.value
        type_ = ObjectReferenceType(refers_to=class_name)
        return type_


@bytecode('athrow')
class Throw(Instructor):
    def execute(self):
        obj = self.peek_op_stack()
        return Actions(
            actions.ThrowObject(obj)
        )
