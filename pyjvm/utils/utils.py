"""Miscellaneous useful functions"""
from jawa.util.bytecode import Operand, OperandTypes

from pyjvm.core.jvm_types import Integer


def dump_class(cf, echo):
    """Display information about a class file

    Complements the functionality of the JDK javap tool.
    :param cf: A ClassFile
    :param echo: A print-like method
    """
    echo(f'{cf.this.name.value} : {cf.super_.name.value}')
    for field in cf.fields:
        echo(f'\t{field.name.value}: {field.type}')
    for method in cf.methods:
        echo(f'{method} {method.descriptor.value}')
        if method.code is not None:
            for instruction in method.code.disassemble():
                echo('\t' + str(instruction))
            for ex in method.code.exception_table:
                print(ex)
    echo()
    for constant in cf.constants:
        echo(constant)


def split_by_predicate(iterable, predicate):
    """Split an iterable into two lists the according to a predicate

    Return a tuple of two lists:
    The first has the values for which `predicate` returned True
    The second has the values for which `predicate` returned False

    :param iterable: An Iterable[T]
    :param predicate: A function from T to bool
    """
    true, false = [], []
    for item in iterable:
        if predicate(item):
            true.append(item)
        else:
            false.append(item)

    return true, false


def class_as_descriptor(name):
    """Return the JVM descriptor for the class `name`"""
    if not name.endswith(';'):
        return 'L' + name + ';'
    else:
        return name


def literal_operand(value):
    """Create an Instruction Operand with type LITERAL and value `value`"""
    return Operand(OperandTypes.LITERAL, value)


def constant_operand(const):
    """Create an Instruction Operand with type CONSTANT_INDEX and value `const.index`"""
    return Operand(OperandTypes.CONSTANT_INDEX, const.index)


def local_operand(index):
    """Create an Instruction Operand with type LOCAL_INDEX and value `index`"""
    return Operand(OperandTypes.LOCAL_INDEX, index)


def pull_pairs(flat):
    """Return a Iterable of pairs of adjacent items in another Iterable

    `flat` should be of even size:
    `len(list(flat)) % 2 == 0`

    >>> list(pull_pairs([1, 2, 3, 4]))
    [(1, 2), (3, 4)]
    """
    it = iter(flat)
    return zip(it, it)


TRUE = Integer.create_instance(1)
FALSE = Integer.create_instance(0)


def bool_to_num(b):
    if b:
        return TRUE
    else:
        return FALSE


def field_name_from_field_ref(ref):
    """Return the class name of the name_and_type attribute of field references

    The need arises from a weird difference between test behaviour and real class file behaviour.
    This suggests that I'm not creating the reference properly in tests.
    But I'm not sure exactly how.

    Maintainers are welcome to solve this issue.
    """
    name = ref.name_and_type.name.value
    try:
        return name.value
    except AttributeError:
        return name


def named_tuple_replace(instance, **kwargs):
    # noinspection PyProtectedMember
    return instance._replace(**kwargs)
