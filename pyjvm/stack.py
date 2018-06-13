class OpStack:
    def __init__(self, max_depth):
        self._values = []
        self._max_depth = max_depth

    def pop(self):
        return self._values.pop(0)

    def push(self, value):
        return self._values.insert(0, value)
