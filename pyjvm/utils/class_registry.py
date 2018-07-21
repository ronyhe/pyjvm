from collections import namedtuple

_ClassInit = namedtuple('_ClassInit', 'the_class, args, kwargs')


class ClassRegistry:
    def __init__(self):
        self._mapping = dict()

    def add(self, name, the_class, *args, **kwargs):
        init = _ClassInit(the_class, args, kwargs)
        if name in self._mapping:
            raise ValueError(f'{name} is already in the class registry')
        self._mapping[name] = init

    def get(self, name, *args, **kwargs):
        try:
            init = self._mapping[name]
        except KeyError as e:
            raise KeyError(f'{name} does not exist in the class registry') from e
        else:
            args = args + init.args
            kwargs.update(init.kwargs)
            return init.the_class(*args, **kwargs)

    def decorator(self, name, *args, **kwargs):
        def wrapper(a_class):
            self.add(name, a_class, *args, **kwargs)
            return a_class

        return wrapper

    def keys(self):
        return self._mapping.keys()
