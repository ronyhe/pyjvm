from pathlib import Path

from jawa.cf import ClassFile
from jawa.util.bytecode import Operand, OperandTypes


def dump_class(path, echo):
    path = Path(path)
    with path.open(mode='rb') as file:
        cf = ClassFile(file)
        echo(cf.this)
        for field in cf.fields:
            echo(field)
        for method in cf.methods:
            echo(method)
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


def pull_pairs(flat):
    it = iter(flat)
    return zip(it, it)
