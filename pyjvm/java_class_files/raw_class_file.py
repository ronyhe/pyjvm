from collections import namedtuple
from pathlib import Path

from pyjvm.java_class_files.bytes_parser import BytesParser, FROM_BYTES_PARSER_METHOD_NAME
from pyjvm.java_class_files.raw_attributes import parse_raw_attributes
from pyjvm.java_class_files.raw_constant_pool_entries import _ConstantPoolEntry, parse_constant_pool
from pyjvm.utils import add_class_method

_DATA_FIELDS = 'minor_version, major_version, constant_pool, access_flags, this_class, ' \
              'super_class, interfaces, fields, methods, attributes'


RawJavaClass = namedtuple('RawJavaClass', _DATA_FIELDS)


_JAVA_MAGIC_TEXT = '0xCAFEBABE'
_JAVA_MAGIC_NUMBER = int(_JAVA_MAGIC_TEXT, 16)


def _compound_info_class(name):
    the_class = namedtuple(name, 'access_flags, name_index, descriptor_index, attributes')

    def from_bytes_parser(cls, parser: BytesParser, constant_pool):
        flags, name_index, descriptor_index, attributes_count = (parser.u2() for _ in range(4))
        attributes = parse_raw_attributes(parser, constant_pool, attributes_count)
        return cls(flags, name_index, descriptor_index, attributes)

    add_class_method(the_class, FROM_BYTES_PARSER_METHOD_NAME, from_bytes_parser)
    return the_class


RawFieldInfo = _compound_info_class('RawFieldInfo')
RawMethodInfo = _compound_info_class('RawMethodInfo')


class IllegalClassFileData(BaseException):
    def __init__(self, message):
        super().__init__(message)


class _Parser(BytesParser):
    def parse(self):
        try:
            return self._parse()
        except IllegalClassFileData as e:
            raise e
        except Exception as e:
            raise IllegalClassFileData('Error while parsing class file') from e

    def _parse(self):
        self.magic_number()
        minor_version, major_version, constant_pool_count = self.indices(3)
        constant_pool = self.parse_constant_pool(constant_pool_count)
        access_flags, this_class, super_class, interfaces_count = self.indices(4)
        interfaces = tuple(self.indices(interfaces_count))

        field_count = self.u2()
        # noinspection PyUnresolvedReferences
        fields = tuple(RawFieldInfo.from_bytes_parser(self, constant_pool) for _ in range(field_count))

        method_count = self.u2()
        # noinspection PyUnresolvedReferences
        methods = tuple(RawMethodInfo.from_bytes_parser(self, constant_pool) for _ in range(method_count))

        attribute_count = self.u2()
        attributes = parse_raw_attributes(self, constant_pool, attribute_count)

        return RawJavaClass(
            minor_version=minor_version,
            major_version=major_version,
            constant_pool=constant_pool,
            access_flags=access_flags,
            interfaces=interfaces,
            fields=fields,
            methods=methods,
            this_class=this_class,
            super_class=super_class,
            attributes=attributes
        )

    def indices(self, amount):
        for _ in range(amount):
            yield self.u2()

    def parse_constant_pool(self, constant_pool_count):
        return parse_constant_pool(self, constant_pool_count)

    def parse_constant_pool_entry(self):
        # noinspection PyUnresolvedReferences
        return _ConstantPoolEntry.from_bytes_parser(self)

    def parse_constant_pool_index(self):
        return self.u2()

    def from_self(self, the_bytes_class):
        return the_bytes_class.from_bytes_parser(self)

    def parse_utf_8(self):
        length_in_bytes = self.u2()
        return self.modified_utf_8_string(length_in_bytes)

    def magic_number(self):
        magic = self.u4()
        message = f'Java class files must start with the java magic number: {_JAVA_MAGIC_TEXT}'
        self.assertion(magic == _JAVA_MAGIC_NUMBER, message)

    @staticmethod
    def assertion(condition, message):
        if not condition:
            raise IllegalClassFileData(message)


def parse_bytes(the_bytes):
    parser = _Parser(the_bytes)
    return parser.parse()


def parse_file(file_path):
    path = Path(file_path)
    with path.open(mode='rb') as file:
        parser = _Parser(file.read())
        return parser.parse()
