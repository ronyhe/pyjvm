from pyjvm.java_class_files.bytes_parser import bytes_class, U2

DEFAULT_VALUE_NAME = 'value'

INDEX = U2


def single_index_class(name):
    return bytes_class(name, (
        (DEFAULT_VALUE_NAME, INDEX),
    ))


def multiple_indices_class(name, index_names):
    return bytes_class(name, (
        (index_name, INDEX) for index_name in index_names
    ))


def single_value_class(class_name, value_spec):
    return bytes_class(class_name, (
        (DEFAULT_VALUE_NAME, value_spec),
    ))


def class_and_name_and_type_indexes_class(name):
    return bytes_class(name, (
        ('class_index', INDEX),
        ('name_and_type_index', INDEX)
    ))
