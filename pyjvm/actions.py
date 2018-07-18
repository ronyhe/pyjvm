import attr


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


@attr.s
class IncrementProgramCounter(Action):
    @classmethod
    def after(cls, *actions):
        acts = list(actions)
        acts.append(cls())
        return Actions(*acts)


@attr.s(frozen=True)
class StoreInLocals(Action):
    index = attr.ib()
    value = attr.ib()

    def __iter__(self):
        yield self.index
        yield self.value


@attr.s(frozen=True)
class Pop(Action):
    amount = attr.ib(default=1)


@attr.s(frozen=True)
class StoreIntoArray(Action):
    array = attr.ib()
    index = attr.ib()
    value = attr.ib()


@attr.s(frozen=True)
class Push(Action):
    value = attr.ib()


@attr.s(frozen=True)
class PushMany(Action):
    values = attr.ib(factory=tuple, converter=tuple)


@attr.s(frozen=True)
class DuplicateTop(Action):
    amount_to_take = attr.ib()
    index_for_insertion = attr.ib()


@attr.s(frozen=True)
class ThrowNullPointerException(Action):
    pass


@attr.s(frozen=True)
class ThrowNegativeArraySizeException(Action):
    pass


@attr.s(frozen=True)
class ThrowCheckCastException(Action):
    pass


@attr.s(frozen=True)
class ThrowObject(Action):
    value = attr.ib()


@attr.s(frozen=True)
class PushNewInstance(Action):
    class_ = attr.ib()


@attr.s(frozen=True)
class PutField(Action):
    object_ = attr.ib()
    field_name = attr.ib()
    value = attr.ib()


@attr.s(frozen=True)
class PutStatic(Action):
    class_name = attr.ib()
    field_name = attr.ib()
    value = attr.ib()


@attr.s(frozen=True)
class Invoke(Action):
    class_name = attr.ib()
    method_name = attr.ib()
    arguments = attr.ib(converter=tuple)


@attr.s(frozen=True)
class ReturnResult(Action):
    result = attr.ib()
