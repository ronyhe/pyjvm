from pyjvm.model.jvm_types import Integer, Long, Float, Double

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
    return _BY_TYPE[type_]


def type_by_indicator(indicator):
    return _BY_INDICATOR[indicator]
