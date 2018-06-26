from pathlib import Path

from jawa.cf import ClassFile


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
        echo()
        for constant in cf.constants:
            echo(constant)
