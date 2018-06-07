class TagRegistry:
    def __init__(self):
        self.dict = dict()

    def register(self, key, value):
        self.dict[key] = value

    def decorator(self, key):
        def func(value):
            self.register(key, value)
            return value

        return func

    def get(self, key):
        try:
            return self.dict[key]
        except LookupError as error:
            raise LookupError(f'No class registered for tag {key}') from error
