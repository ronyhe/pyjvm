class ConstantPool:
    MISSING_INDEX = object()

    def __init__(self):
        self._list = []

    def add(self, value, indices=1):
        if indices < 1:
            raise ValueError('Indices must be positive')
        self._list.append(value)
        for _ in range(indices - 1):
            self._list.append(self.MISSING_INDEX)

    def add_double_index(self, value):
        self.add(value, indices=2)

    def at_dumb_java_index(self, index):
        try:
            entry = self._list[index]
        except LookupError:
            raise IndexError(f'No entry at index {index}. Are you out of bounds?')
        else:
            if entry is self.MISSING_INDEX:
                raise IndexError(f'There is no entry at {index}. A previous entry holds more than one index')
            return entry

    def __iter__(self):
        for entry in self._list:
            if entry is not self.MISSING_INDEX:
                yield entry

    def _string_helper(self, content):
        return f'{self.__class__.__name__}({content})'

    def __repr__(self):
        return str(self)

    def __str__(self):
        content = ',\n'.join(str(item) for item in self._list)
        return self._string_helper(content)
