from typing import Generic, TypeVar

T = TypeVar('T')


class Stack(Generic[T]):
    def __init__(self, values=None, max_depth=None):
        self.max_depth = max_depth
        self._values = []
        if values is not None:
            for value in reversed(values):
                self.push(value)

    def pop(self) -> T:
        return self._values.pop(0)

    def push(self, value: T):
        if self.max_depth is not None and len(self._values) == self.max_depth:
            raise OverflowError('Max amount of values in stack, cannot add more')
        return self._values.insert(0, value)

    def insert_at_offset(self, offset, value):
        if offset < 0:
            raise ValueError('Offset must be >= 0')
        current_size = self.size()
        if current_size < offset - 1:
            raise IndexError(f'Cannot insert to stack at offset {offset} '
                             f'because the current size of the stack is {current_size}')
        self._values.insert(offset, value)

    def peek(self, index=0) -> T:
        return self._values[index]

    def peek_many(self, amount):
        if amount < 0:
            raise ValueError('Peek amount muse be >= 0')
        return self._values[:amount]

    def size(self) -> int:
        return len(self._values)

    def __iter__(self):
        return iter(self._values)
