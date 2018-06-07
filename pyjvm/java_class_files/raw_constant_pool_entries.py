import enum
from collections import namedtuple, OrderedDict

from pyjvm.java_class_files.bytes_class_factories import single_index_class, multiple_indices_class, \
    single_value_class, class_and_name_and_type_indexes_class, INDEX, DEFAULT_VALUE_NAME
from pyjvm.java_class_files.bytes_parser import bytes_class, DOUBLE, U4, FLOAT, U1, LONG, BytesParser
from pyjvm.java_class_files.constant_pool import ConstantPool
from pyjvm.java_class_files.tag_registry import TagRegistry


class ConstantTags(enum.Enum):
    CLASS = 7
    FIELD_REF = 9
    METHOD_REF = 10
    INTERFACE_METHOD_REF = 11
    STRING = 8
    INTEGER = 3
    FLOAT = 4
    LONG = 5
    DOUBLE = 6
    NAME_AND_TYPE = 12
    UTF_8 = 1
    METHOD_HANDLE = 15
    METHOD_TYPE = 16
    INVOKE_DYNAMIC = 18


TAGS_THAT_TAKE_TWO_INDICES = ConstantTags.LONG, ConstantTags.DOUBLE

CONSTANT_CLASSES_REGISTRY = TagRegistry()
tagged = CONSTANT_CLASSES_REGISTRY.decorator


@tagged(ConstantTags.INTEGER)
class RawIntegerInfo(single_value_class('RawIntegerInfo', U4)):
    pass


@tagged(ConstantTags.LONG)
class RawLongInfo(single_value_class('RawLongInfo', LONG)):
    pass


@tagged(ConstantTags.FLOAT)
class RawFloatInfo(single_value_class('RawFloatInfo', FLOAT)):
    pass


@tagged(ConstantTags.DOUBLE)
class RawDoubleInfo(single_value_class('RawDoubleInfo', DOUBLE)):
    pass


@tagged(ConstantTags.CLASS)
class RawClassInfo(single_index_class('RawClassInfo')):
    pass


@tagged(ConstantTags.FIELD_REF)
class RawFieldRefInfo(class_and_name_and_type_indexes_class('RawFieldRefInfo')):
    pass


@tagged(ConstantTags.METHOD_REF)
class RawMethodRefInfo(class_and_name_and_type_indexes_class('RawMethodRefInfo')):
    pass


@tagged(ConstantTags.INTERFACE_METHOD_REF)
class RawInterfaceMethodRefInfo(class_and_name_and_type_indexes_class('RawInterfaceMethodRefInfo')):
    pass


@tagged(ConstantTags.STRING)
class RawStringInfo(single_index_class('RawStringInfo')):
    pass


@tagged(ConstantTags.NAME_AND_TYPE)
class RawNameAndTypeInfo(multiple_indices_class('RawNameAndTypeInfo', 'name_index descriptor_index'.split())):
    pass


@tagged(ConstantTags.METHOD_HANDLE)
class RawMethodHandleInfo(bytes_class('RawMethodHandleInfo', (
        ('ref_kind', U1),
        ('ref_index', INDEX)
))):
    pass


@tagged(ConstantTags.METHOD_TYPE)
class RawMethodTypeInfo(single_index_class('RawMethodTypeInfo')):
    pass


@tagged(ConstantTags.INVOKE_DYNAMIC)
class RawInvokeDynamicInfo(multiple_indices_class('RawInvokeDynamicInfo',
                                                  'bootstrap_method_attr_index name_and_type_index'.split())):
    pass


@tagged(ConstantTags.UTF_8)
class RawUtf8Info(namedtuple('RawUtf8Info', DEFAULT_VALUE_NAME)):
    @classmethod
    def from_bytes_parser(cls, parser: BytesParser):
        amount_of_bytes = parser.u2()
        value = parser.modified_utf_8_string(amount_of_bytes)
        return cls(value)


class ConstantPoolEntry(namedtuple('ConstantPoolEntry', 'tag, info')):
    @classmethod
    def from_bytes_parser(cls, parser):
        raw_tag = parser.u1()
        tag = ConstantTags(raw_tag)
        the_class = CONSTANT_CLASSES_REGISTRY.get(tag)
        info = the_class.from_bytes_parser(parser)
        result = cls(tag, info)
        return result


def parse_constant_pool(parser: BytesParser, length):
    remaining = length - 1
    pool = ConstantPool()
    while not remaining == 0:
        # noinspection PyUnresolvedReferences
        entry = ConstantPoolEntry.from_bytes_parser(parser)
        if entry.tag in TAGS_THAT_TAKE_TWO_INDICES:
            indices = 2
        else:
            indices = 1

        remaining -= indices
        pool.add(entry.info, indices=indices)

    return pool
