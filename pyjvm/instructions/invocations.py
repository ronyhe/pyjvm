from pyjvm.core import actions
from pyjvm.core.actions import Actions
from pyjvm.instructions.instructions import bytecode, Instructor
from pyjvm.utils.jawa_conversions import key_from_method_ref


@bytecode('invokevirtual', 1)
@bytecode('invokespecial', 1)
@bytecode('invokeinterface', 1)
@bytecode('invokestatic', 0)
class InvokeVirtual(Instructor):
    """Invokes methods

    This Instructor uses the method's details to figure out how many parameters should be popped of the stack.
    It also provides an `args_to_add` method to enable popping off the implicit `this` parameter for instance methods.

    So the general process is:
     - Get a reference to the method via the details in the instruction
     - Extract number of parameters and add `args_to_add` to it
     - Pop parameters and invoke with them
    """

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
        args = reversed(self.peek_many(num_args))

        return Actions(
            actions.Pop(num_args),
            actions.Invoke(class_name, key, args)
        )
