import functools

from pyjvm.jvm_types import Integer, Float, Long, Double

_VALUE_MESSAGE = 'Value {value} was expected to have type {expected}, instead it has type {actual}'
_EXPECTED_MESSAGE = 'Value {value} was expected to be a {description}, instead it has type {actual}'


def _verify_value_type(expected, value):
    actual = value.type
    if not actual == expected:
        raise TypeError(_VALUE_MESSAGE.format(value=value, expected=expected, actual=actual))


def _verify_ref(value, condition, description):
    if not condition:
        raise TypeError(_EXPECTED_MESSAGE.format(value=value, description=description, actual=value.type))


verify_integer = functools.partial(_verify_value_type, Integer)

verify_float = functools.partial(_verify_value_type, Float)

verify_long = functools.partial(_verify_value_type, Long)

verify_double = functools.partial(_verify_value_type, Double)


def verify_reference(value):
    _verify_ref(value, value.type.is_reference, 'reference')


def verify_class_reference(value):
    _verify_ref(value, value.type.is_class_reference, 'reference to a class')


def verify_array_reference(value):
    _verify_ref(value, value.type.is_array_reference, 'reference to an array')


def verifier_by_type(type_):
    if type_ == Integer:
        return verify_integer
    elif type_ == Float:
        return verify_float
    elif type_ == Long:
        return verify_long
    elif type_ == Double:
        return verify_double
    elif type_.is_reference:
        return verify_reference
    else:
        raise LookupError(f'No verifier for type {type}')
