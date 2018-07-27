from collections import namedtuple

_ClassInit = namedtuple('_ClassInit', 'the_class, args, kwargs')


class ClassRegistry:
    """A registry for dynamically fetching an creating class instances

    A user can add a class to the registry with a key and later fetch an instance.
    They can specify arguments at registration and/or at fetch time.
    Those arguments will be passed to the class constructor when an instance is created (fetch time).

    >>> class SomeClass:
    ...     def __init__(self, fetch_time, reg_time):
    ...         self.reg_time = reg_time
    ...         self.fetch_time = fetch_time
    ...
    >>> reg = ClassRegistry()
    >>> reg.add('some_name', SomeClass, 'reg')
    >>> instance = reg.get('some_name', 'fetch')
    >>> instance.reg_time
    'reg'
    >>> instance.fetch_time
    'fetch'

    The decorator method can be used to register the class when declaring it:
        .. code::

            @reg.decorator('some_name', 'reg')
            class ClassToRegister:
                pass

    The registry was designed to answer the need to dispatch instructions to their corresponding `Instructor` classes.
    See instructions/instructions.py for a concrete usage example.
    """

    def __init__(self):
        self._mapping = dict()

    def add(self, name, the_class, *args, **kwargs):
        """Register `the_class` with key `name`"""
        init = _ClassInit(the_class, args, kwargs)
        if name in self._mapping:
            raise ValueError(f'{name} is already in the class registry')
        self._mapping[name] = init

    def get(self, name, *args, **kwargs):
        """Return an instance of the class registered under the key `name`

        The instance will be initialized with `*args` followed by the arguments from registry time.
        The keywords to the constructor will be `kwargs` updated with the keyword arguments from registry time.
        """
        try:
            init = self._mapping[name]
        except KeyError as e:
            raise KeyError(f'{name} does not exist in the class registry') from e
        else:
            args = args + init.args
            kwargs.update(init.kwargs)
            return init.the_class(*args, **kwargs)

    def decorator(self, name, *args, **kwargs):
        """Return a function that takes a class an registers it under `name` with the provided arguments"""

        def wrapper(a_class):
            self.add(name, a_class, *args, **kwargs)
            return a_class

        return wrapper

    def keys(self):
        return self._mapping.keys()
