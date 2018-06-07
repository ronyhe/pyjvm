from collections.__init__ import namedtuple

from pyjvm.java_class_files.bytes_class_factories import single_index_class, multiple_indices_class
from pyjvm.java_class_files.bytes_parser import BytesParser
from pyjvm.java_class_files.raw_constant_pool import RawUtf8Info

CONSTANT_VALUE_NAME = 'ConstantValue'
CODE_NAME = 'Code'

RawConstantValueInfo = single_index_class('RawConstantValueInfo')

RawExceptionTableEntryInfo = multiple_indices_class('RawExceptionTableEntryInfo',
                                                    'start_pc end_pc handler_pc catch_type'.split())


RawCodeAttributeInfo = namedtuple('RawCodeAttributeInfo', 'max_stack, max_locals, code, exception_table, attributes')


class _VeryRawAttributeInfo(namedtuple('VeryRawAttributeInfo', 'name_index, value')):
    @classmethod
    def from_bytes_parser(cls, parser: BytesParser):
        name_index = parser.u2()
        amount_of_bytes = parser.u4()
        value = bytes(parser.u1() for _ in range(amount_of_bytes))
        return cls(name_index, value)


# noinspection PyUnusedLocal
def _parser_constant_value_attribute(parser, constant_pool):
    return RawConstantValueInfo.from_bytes_parser(parser)


def _parse_code_attribute(parser, constant_pool):
    max_stack = parser.u2()
    max_locals = parser.u2()
    code_length = parser.u4()
    code = tuple(parser.u1() for _ in range(code_length))
    exception_table_length = parser.u2()
    exception_table = tuple(RawExceptionTableEntryInfo.from_bytes_parser(parser)
                            for _ in range(exception_table_length))
    attribute_count = parser.u2()
    attributes = parse_raw_attributes(parser, constant_pool, attribute_count)
    return RawCodeAttributeInfo(
        max_stack=max_stack,
        max_locals=max_locals,
        code=code,
        exception_table=exception_table,
        attributes=attributes
    )


def _interpret(attribute, constant_pool):
    name_index, value = attribute
    name_entry = constant_pool.at_dumb_java_index(name_index)
    if not isinstance(name_entry, RawUtf8Info):
        raise TypeError('The name_index of an attribute must point to RawUtf8Info')
    name = name_entry.value
    data = attribute.value
    parser = BytesParser(data)
    if name == CODE_NAME:
        return _parse_code_attribute(parser, constant_pool)
    elif name == CONSTANT_VALUE_NAME:
        return _parser_constant_value_attribute(parser, constant_pool)
    else:
        return None


def parse_raw_attributes(parser: BytesParser, constant_pool, count):
    very_raw = (_VeryRawAttributeInfo.from_bytes_parser(parser) for _ in range(count))
    # noinspection PyTypeChecker
    less_raw = (_interpret(raw, constant_pool) for raw in very_raw)
    return tuple(raw for raw in less_raw if raw is not None)
