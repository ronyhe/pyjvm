from pyjvm import actions
from pyjvm.actions import IncrementProgramCounter
from pyjvm.instructions.instructions import bytecode, Instructor


@bytecode('invokevirtual')
class InvokeVirtual(Instructor):
    def execute(self):
        method_ref = self.operand_as_constant()
        class_name = method_ref.class_.name.value
        method_name = method_ref.name_and_type.name.value
        class_= self.loader.get_the_class(class_name)
        method = class_.methods[method_name]
        num_args = len(method.args) + 1  # Implicit `this` parameter
        args = self.peek_many(num_args)

        return IncrementProgramCounter.after(
            actions.Pop(num_args),
            actions.Invoke(class_name, method_name, args)
        )
