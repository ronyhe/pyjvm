from pyjvm.class_registry import ClassRegistry

_registry = ClassRegistry()

bytecode = _registry.decorator


class InstructorInputs:
    # noinspection PyShadowingBuiltins
    def __init__(self, *, instruction, locals, op_stack, constants):
        self.instruction = instruction
        self.locals = locals
        self.op_stack = op_stack
        self.constants = constants


class Instructor:
    def __init__(self, inputs):
        self.instruction = inputs.instruction
        self.locals = inputs.locals
        self.op_stack = inputs.op_stack
        self.constants = inputs.constants

    def execute(self):
        raise NotImplementedError()

    def operand_as_int(self, index=0):
        return int(self.instruction.operands[index].value)

    def peek_op_stack(self, *args, **kwargs):
        return self.op_stack.peek(*args, *kwargs)


def execute_instruction(inputs):
    instruction_name = inputs.instruction.mnemonic
    executor = _registry.get(instruction_name, inputs)
    return executor.execute()


def get_implemented_instructions():
    return _registry.keys()


# noinspection PyUnresolvedReferences
from pyjvm.instructions import stores
