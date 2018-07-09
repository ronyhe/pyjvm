class Action:
    pass


class Actions:
    def __init__(self, *actions):
        self.actions = tuple(actions)

    def has(self, *actions):
        types = self._types()
        return all(self._has_action(ac, types) for ac in actions)

    def __contains__(self, item):
        return self.has(item)

    def __iter__(self):
        return iter(self.actions)

    def __eq__(self, other):
        try:
            return self.actions == other.actions
        except AttributeError:
            return False

    def __hash__(self):
        return hash(self.actions)

    def __repr__(self):
        elements = ', '.join(repr(ac) for ac in self.actions)
        return f'Actions({elements})'

    def _has_action(self, action, types):
        specific = action in self.actions
        if specific:
            return specific

        try:
            return action in types
        except TypeError:
            return False

    def _types(self):
        def get_type(obj):
            if isinstance(obj, type):
                return obj
            else:
                return type(obj)

        return set(get_type(ac) for ac in self.actions)


class IncrementProgramCounter(Action):
    @classmethod
    def after(cls, *actions):
        acts = list(actions)
        acts.append(cls())
        return Actions(*acts)

    def __repr__(self):
        return self.__class__.__name__


class StoreInLocals(Action):
    def __init__(self, *, index, value):
        self.index = index
        self.value = value

    def __eq__(self, other):
        try:
            return self.index == other.index and self.value == other.value
        except AttributeError:
            return False

    def __iter__(self):
        yield self.index
        yield self.value

    def __hash__(self):
        elements = self.__class__, self.index, self.value
        return hash(elements)

    def __repr__(self):
        return f'{self.__class__.__name__}(index={self.index}, value={repr(self.value)})'


class Pop(Action):
    def __init__(self, amount=1):
        self.amount = amount

    def __eq__(self, other):
        try:
            return self.amount == other.amount
        except AttributeError:
            return False

    def __hash__(self):
        elements = self.__class__, self.amount
        return hash(elements)

    def __repr__(self):
        return f'{self.__class__.__name__}({self.amount})'


class StoreIntoArray(Action):
    def __init__(self, *, array, index, value):
        self.array = array
        self.index = index
        self.value = value

    def __eq__(self, other):
        try:
            return self.array == other.array and self.index == other.index and self.value == other.value
        except AttributeError:
            return False

    def __hash__(self):
        elements = self.__class__, self.array, self.index, self.value
        return hash(elements)

    def __repr__(self):
        return f'{self.__class__.__name__}(array={self.array}, index={self.index}, value={self.value})'
