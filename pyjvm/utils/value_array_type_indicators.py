"""Functions for converting types to indicators and vice versa

The JVM array instructions indicate value types using specific integers.
See instructions/references.py for usage examples.
"""
from pyjvm.core.jvm_types import Integer, Long, Float, Double

_BY_TYPE = {
    Integer: 10,
    Long: 11,
    Float: 6,
    Double: 7
}

_BY_INDICATOR = {v: k for k, v in _BY_TYPE.items()}
_BY_INDICATOR.update({
    4: Integer,
    5: Integer,
    8: Integer,
    9: Integer
})


def indicator_by_type(type_):
    """Return the int that corresponds to `type_`"""
    return _BY_TYPE[type_]


def type_by_indicator(indicator):
    """Return the type that corresponds to `indicator`"""
    return _BY_INDICATOR[indicator]
