class ClassLoader:
    def get_by_name(self, name):
        raise NotImplementedError()


class FixedClassLoader(ClassLoader):
    def __init__(self, classes):
        self.classes = dict(classes)

    def get_by_name(self, name):
        return self.classes[name]
