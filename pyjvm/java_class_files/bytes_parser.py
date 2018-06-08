from collections import namedtuple
from struct import Struct

from pyjvm.java_class_files.modified_utf_8 import decode_modified_utf8
from pyjvm.utils.utils import unzip, add_class_method


def _format(format_string) -> Struct:
    return Struct('>' + format_string)


U1 = _format('B')
U2 = _format('H')
U4 = _format('I')
FLOAT = _format('f')
DOUBLE = _format('d')
LONG = _format('q')


FROM_BYTES_PARSER_METHOD_NAME = 'from_bytes_parser'


class BytesParser:
    def __init__(self, iterable_bytes):
        self._inputs = bytes(iterable_bytes)

    def _assert_bytes_left(self, amount):
        bytes_left = len(self._inputs)
        if bytes_left < amount:
            raise IndexError(f'Attempted to parse {amount} bytes, but only {bytes_left} remaining')

    def _take_bytes(self, amount):
        self._assert_bytes_left(amount)
        inputs = self._inputs

        the_bytes = inputs[:amount]
        self._inputs = inputs[amount:]

        return the_bytes

    # noinspection SpellCheckingInspection
    def unpack(self, struct: Struct):
        the_bytes = self._take_bytes(struct.size)
        return struct.unpack(the_bytes)[0]

    def u1(self):
        return self.unpack(U1)

    def u2(self):
        return self.unpack(U2)

    def u4(self):
        return self.unpack(U4)

    def float(self):
        return self.unpack(FLOAT)

    def double(self):
        return self.unpack(DOUBLE)

    def long(self):
        return self.unpack(LONG)

    def modified_utf_8_string(self, amount_of_bytes):
        the_bytes = self._take_bytes(amount_of_bytes)
        return decode_modified_utf8(the_bytes)


def bytes_class(name, members_with_specs):
    names, specs = unzip(members_with_specs)
    the_class = namedtuple(name, names)

    def from_bytes_parser(cls, parser: BytesParser):
        # noinspection PyProtectedMember
        values = (parser.unpack(spec) for spec in specs)
        return cls(*values)

    add_class_method(the_class, FROM_BYTES_PARSER_METHOD_NAME, from_bytes_parser)

    return the_class
