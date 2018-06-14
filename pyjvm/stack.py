from typing import Generic, TypeVar

T = TypeVar('T')


class Stack(Generic[T]):
    def __init__(self, max_depth=None):
        self._values = []
        self.max_depth = max_depth

    def pop(self) -> T:
        return self._values.pop(0)

    def push(self, value: T):
        if self.max_depth is not None and len(self._values) == self.max_depth:
            raise OverflowError('Max amount of values in stack, cannot add more')
        return self._values.insert(0, value)

    def peek(self) -> T:
        return self._values[0]
