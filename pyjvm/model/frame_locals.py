class Locals:
    """A local variable array for Frame objects

    The main reason for a class, rather than a simple list, is that certain JVM types are expected
    to hold two slots in this array.
    This class aims to preserves that guarantee by using an internal `MISSING` object to mark inaccessible slots.
    It also prevents uninitialized access at runtime.
    However, a class that was emitted by a compliant Java compiler should already prevent such code from existing.
    """

    MISSING = object()

    def __init__(self, length):
        if length < 0:
            raise ValueError(f'{self.__class__.__name__} must have a positive length')
        self.length = length
        self._locals: list = [None] * length

    def store(self, index, value):
        """Store `value` at `index`"""
        if value is None:
            raise ValueError('Cannot store None in locals')
        self._locals[index] = value
        if value.type.needs_two_slots:
            self._locals[index + 1] = self.MISSING

    def load(self, index):
        """Load the value at `index`"""
        result = self._locals[index]
        if result is None:
            raise ValueError(f'Access to uninitialized local variable at index {index}')
        if result is self.MISSING:
            message = f'Access to no-access local index {index}. Perhaps a previous value holds more than one index'
            raise ValueError(message)
        return result
