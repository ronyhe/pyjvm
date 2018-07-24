from pyjvm import actions
from pyjvm.actions import Actions
from pyjvm.instructions.instructions import bytecode, Instructor
from pyjvm.model.jvm_class import MethodKey
from pyjvm.utils.jawa_conversions import key_from_method_ref


@bytecode('invokevirtual', 1)
@bytecode('invokespecial', 1)
@bytecode('invokeinterface', 1)
@bytecode('invokestatic', 0)
class InvokeVirtual(Instructor):
    def __init__(self, inputs, args_to_add):
        super().__init__(inputs)
        self.args_to_add = args_to_add

    def execute(self):
        method_ref = self.operand_as_constant()
        class_name = method_ref.class_.name.value
        key = key_from_method_ref(method_ref)

        class_ = self.loader.get_the_class(class_name)
        method = class_.methods[key]
        num_args = len(method.args) + self.args_to_add
        args = self.peek_many(num_args)

        return Actions(
            actions.Pop(num_args),
            actions.Invoke(class_name, key, args)
        )
