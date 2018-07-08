from jawa.util.bytecode import Instruction

from pyjvm.class_registry import ClassRegistry

_registry = ClassRegistry()

bytecode = _registry.decorator


class Executor:
    def __init__(self, instruction, machine):
        self.instruction: Instruction = instruction
        self.machine = machine

    def execute(self):
        raise NotImplementedError()


def execute_instruction(instruction, machine):
    executor = _registry.get(instruction.mnemonic, instruction, machine)
    return executor.execute()


def get_implemented_instructions():
    return _registry.keys()
