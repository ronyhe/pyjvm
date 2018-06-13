import enum
from collections import namedtuple

# noinspection SpellCheckingInspection
DESCRIPTOR_BASE_TYPES_THAT_ARE_ACTUALLY_INTEGERS = 'BCSIZ'

ImpType = namedtuple('ImpType', 'name, letter, double_index')


class ImpTypes(enum.Enum):
    Integer = ImpType('Integer', 'I', double_index=False)
    Float = ImpType('Float', 'F', double_index=False)
    Double = ImpType('Double', 'D', double_index=True)
    Long = ImpType('Long', 'J', double_index=True)
    Reference = ImpType('Reference', 'L', double_index=False)

    @classmethod
    def from_letter(cls, letter):
        letter = letter.upper()
        if letter in DESCRIPTOR_BASE_TYPES_THAT_ARE_ACTUALLY_INTEGERS:
            return cls.Integer
        else:
            for imp in cls:
                if imp.letter == letter:
                    return imp

            raise ValueError(f'No implementation type for {letter}')


Value = namedtuple('Value', 'imp_type, value')
