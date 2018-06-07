# noinspection SpellCheckingInspection
def unzip(pairs):
    the_as, the_bs = [], []
    for a, b in pairs:
        the_as.append(a)
        the_bs.append(b)

    return the_as, the_bs


def add_class_method(the_class, method_name, method):
    setattr(the_class, method_name, classmethod(method))
