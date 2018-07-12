from pyjvm import actions
from pyjvm.actions import IncrementProgramCounter
from pyjvm.hierarchies import is_value_instance_of
from pyjvm.instructions.instructions import bytecode, Instructor
from pyjvm.jvm_types import Integer
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
