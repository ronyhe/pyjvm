import attr


class Action:
    """An object representing operations in a Machine

    This class registers sub classes solely for reporting purposes (see main.py).
    """
    _subs = []

    def __init_subclass__(cls, **kwargs):
        cls._subs.append(cls.__name__)

    @classmethod
    def action_names(cls):
        """Return the named of all sub classes of this class"""
        return tuple(cls._subs)


class Actions:
    """A collection of `Action` instance"""

    def __init__(self, *actions):
        """Return a new `Actions` instance

        :param actions: Iterable[Action] the actions in this collection
        """
        self.actions = tuple(actions)

    def has(self, *actions):
        """Return True if this instance has all `actions`, False otherwise

        Any action in `action` can be an action type instead of an instance.
        If this instance has an instance of that type, it will treat that action as existing.
        Actual instances will be fully compared to check for existence.
        """
        types = self._types()
        return all(self._has_action(ac, types) for ac in actions)

    def __contains__(self, item):
        return self.has([item])

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
        """Return True if `action` is in this instance, False otherwise

        This method follows is a utility for the `has` method and it follows that method's description.
        """
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
    """The basic action of moving to the next instruction"""

    @classmethod
    def after(cls, *actions):
        """Return an `Actions` instance that contains `actions` followed by an instance of this class"""
        acts = list(actions)
        acts.append(cls())
        return Actions(*acts)


@attr.s(frozen=True)
class Push(Action):
    """Push `value` onto the current frame's op stack

    Presumably, `value` will be a JvmValue
    """
    value = attr.ib()


@attr.s(frozen=True)
class Pop(Action):
    """Remove the top `amount` values from the current frame's op stack"""
    amount = attr.ib(default=1)


@attr.s(frozen=True)
class PushNewInstance(Action):
    """Create a new instance of the JvmClass `class_` and push that instance onto the current frame's op stack"""
    class_ = attr.ib()

    def __str__(self):
        return f'{self.__class__.__name__}({self.class_.name})'


@attr.s(frozen=True)
class DuplicateTop(Action):
    """Duplicate and reinsert values at the top of the current frame's op stack

    amount_to_take: int, the amount of top values to duplicate
    index_for_insertion: int, the offset from the top at which to insert the duplicates
    """
    amount_to_take = attr.ib()
    index_for_insertion = attr.ib()


@attr.s(frozen=True)
class StoreInLocals(Action):
    """Store `value` into the current frame's Locals array at `index`"""
    index = attr.ib()
    value = attr.ib()


@attr.s(frozen=True)
class StoreIntoArray(Action):
    """Store `value` in `array` at `index`"""
    array = attr.ib()
    index = attr.ib()
    value = attr.ib()


@attr.s(frozen=True)
class ThrowObject(Action):
    """Throw `value` as an exception

    `value` is presumed to be derived from `java/lang/Throwable`
    """
    value = attr.ib()


@attr.s(frozen=True)
class CreateAndThrow(Action):
    """Create an instance of the class the name `class_name` and throw that instance as an exception

    `class_name` is presumed to be derived from `java/lang/Throwable`
    """
    class_name = attr.ib()


@attr.s(frozen=True)
class PutField(Action):
    """Store `value` in `object` at the instanfce field named `field_name`"""
    object_ = attr.ib()
    field_name = attr.ib()
    value = attr.ib()


@attr.s(frozen=True)
class PutStatic(Action):
    """Store `value` in the static field named `field_name` of the class named `class_name`"""
    class_name = attr.ib()
    field_name = attr.ib()
    value = attr.ib()


@attr.s(frozen=True)
class Invoke(Action):
    """Invoke the method with the key `method_key` in the class named `class_name` and send `arguments` as parameters

    class_name: str
    method_key: MethodKey
    arguments: Iterable[JvmValue]
    """
    class_name = attr.ib()
    method_key = attr.ib()
    arguments = attr.ib(converter=tuple)


@attr.s(frozen=True)
class ReturnResult(Action):
    """Return from the current frame with the result `result`"""
    result = attr.ib()


@attr.s(frozen=True)
class ReturnVoid(Action):
    """Return from the current frame without a result"""
    pass


@attr.s(frozen=True)
class GoTo(Action):
    """Jump to the instruction with the index `target` in the current frame"""
    target = attr.ib(converter=int)


def _throw_built_in(name):
    return CreateAndThrow('java/lang/' + name)


def throw_null_pointer():
    """Return a CreateAndThrow Action for the class `java/lang/NullPointerException`"""
    return _throw_built_in('NullPointerException')


def throw_check_cast():
    """Return a CreateAndThrow Action for the class `java/lang/CheckCastException`"""
    return _throw_built_in('CheckCastException')


def throw_negative_array_size():
    """Return a CreateAndThrow Action for the class `java/lang/NegativeArraySizeException`"""
    return _throw_built_in('NegativeArraySizeException')
