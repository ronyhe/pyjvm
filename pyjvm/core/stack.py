from typing import Generic, TypeVar

T = TypeVar('T')


class Stack(Generic[T]):
    """A simple stack implementation"""

    def __init__(self, values=None, max_depth=None):
        """Return a new Stack instance

        :param values: Iterable[T], initial values that will be pushed onto the stack in reverse order. Defaults to []
        :param max_depth: int, a possible maximum size to conform to at runtime. Defaults to None
        """
        self.max_depth = max_depth
        self._values = []
        if values is not None:
            for value in reversed(values):
                self.push(value)

    def pop(self) -> T:
        """Removes and returns the value on top-of-stack"""
        return self._values.pop(0)

    def push(self, value: T):
        """Push `value` onto stack

        If this stack has a maximum size, and that size is exceeded this method throws a `OverflowError`.
        """
        self._values.insert(0, value)
        self._validate_size()

    def insert_at_offset(self, offset, value):
        """Insert `value` directly at `offset` from top

        If this stack has a maximum size, and that size is exceeded this method throws a `OverflowError`.
        """
        if offset < 0:
            raise ValueError('Offset must be >= 0')
        current_size = self.size()
        if current_size < offset - 1:
            raise IndexError(f'Cannot insert to stack at offset {offset} '
                             f'because the current size of the stack is {current_size}')
        self._values.insert(offset, value)
        self._validate_size()

    def peek(self, index=0) -> T:
        """Return the value at `index` without removing it"""
        return self._values[index]

    def peek_many(self, amount):
        """Return a list with the first `amount` values on the stack"""
        if amount < 0:
            raise ValueError('Peek amount must be >= 0')
        return self._values[:amount]

    def size(self) -> int:
        """Return the amount of values that are currently stored in this stack"""
        return len(self._values)

    def __iter__(self):
        """Return an iterator yielding the values in this stack"""
        return iter(self._values)

    def _validate_size(self):
        if self.max_depth is not None and len(self._values) > self.max_depth + 1:
            raise OverflowError('Max amount of values in stack, cannot add more')
