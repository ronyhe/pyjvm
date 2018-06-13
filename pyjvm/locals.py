from pyjvm.implementation_types import ImpTypes


class Locals:
    MISSING = object()

    def __init__(self, length):
        if length < 0:
            raise ValueError(f'{self.__class__.__name__} must have a positive length')
        self.length = length
        self._locals = [None] * length

    def store(self, index, value):
        if value is None:
            raise ValueError('Cannot store None in locals')
        self._locals[index] = value
        if value.imp_type.double_index:
            # noinspection PyTypeChecker
            self._locals[index + 1] = self.MISSING

    def load(self, index):
        result = self._locals[index]
        if result is None:
            raise ValueError(f'Access to uninitialized local variable at index {index}')
        if result is self.MISSING:
            message = f'Access to no-access local index {index}. Perhaps a previous value holds more than one index'
            raise ValueError(message)
        return result

    def init_with_parameters(self, parameters):
        index = 0
        for p in parameters:
            self.store(index, p)
            index += 1
            if p.imp_type.double_index:
                index += 1
