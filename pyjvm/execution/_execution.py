registry = dict()


class Executor:
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        registry[cls.__name__] = cls()

    def execute(self, instruction, machine):
        raise NotImplementedError()

    def collect_tests(self):
        return [value for name, value in self.__dict__ if name.startwith('test') and callable(value)]


def execute_instruction(instruction, machine):
    executor = registry[instruction.mnemonic]
    return executor.execute(instruction, machine)


def collect_all_tests():
    all_tests = []
    for instance in registry.values():
        all_tests.extend(instance.collect_test())
