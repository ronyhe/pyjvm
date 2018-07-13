from pyjvm import actions, value_array_type_indicators
from pyjvm.actions import IncrementProgramCounter, Actions
from pyjvm.hierarchies import is_value_instance_of
from pyjvm.instructions.instructions import bytecode, Instructor
from pyjvm.jvm_types import Integer, ArrayReferenceType
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


@bytecode('newarray')
class NewValueArray(Instructor):
    def execute(self):
        type_indicator = self.operand_as_int()
        type_ = value_array_type_indicators.type_by_indicator(type_indicator)
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
