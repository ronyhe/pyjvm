from jawa.util.bytecode import Operand, OperandTypes

from pyjvm.model.jvm_types import Integer


def dump_class(cf, echo):
    echo(f'{cf.this.name.value} : {cf.super_.name.value}')
    for field in cf.fields:
        echo(f'\t{field.name.value}: {field.type}')
    for method in cf.methods:
        echo(method)
        if method.code is not None:
            for instruction in method.code.disassemble():
                echo('\t' + str(instruction))
            for ex in method.code.exception_table:
                print(ex)
    echo()
    for constant in cf.constants:
        echo(constant)


def split_by_predicate(iterable, predicate):
    true, false = [], []
    for item in iterable:
        if predicate(item):
            true.append(item)
        else:
            false.append(item)

    return true, false


def class_as_descriptor(name):
    return 'L' + name + ';'


def literal_operand(value):
    return Operand(OperandTypes.LITERAL, value)


def constant_operand(const):
    return Operand(OperandTypes.CONSTANT_INDEX, const.index)


def pull_pairs(flat):
    it = iter(flat)
    return zip(it, it)


TRUE = Integer.create_instance(1)
FALSE = Integer.create_instance(0)


def bool_to_num(b):
    if b:
        return TRUE
    else:
        return FALSE
