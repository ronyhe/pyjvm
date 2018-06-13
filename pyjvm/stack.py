class Stack:
    def __init__(self):
        self._values = []

    def pop(self):
        return self._values.pop(0)

    def push(self, value):
        return self._values.insert(0, value)

    def peek(self):
        return self._values[0]
