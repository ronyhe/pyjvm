registry = dict()


class Executor:
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        registry[cls.__name__] = cls()

    def execute(self, instruction, machine):
        raise NotImplementedError()


def execute_instruction(instruction, machine):
    executor = registry[instruction.mnemonic]
    return executor.execute(instruction, machine)


def collect_all_tests():
    for instance in registry.values():
        yield from instance.collect_tests()


# noinspection PyUnresolvedReferences
from pyjvm.execution import loads
