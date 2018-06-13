from pathlib import Path

from jawa.cf import ClassFile


def dump_class(path):
    path = Path(path)
    with path.open(mode='rb') as file:
        cf = ClassFile(file)
        pool = cf.constants
        for index in range(pool.raw_count):
            try:
                print(f'{index}: {pool[index]}')
            except Exception:
                pass
        print()
        for method in cf.methods:
            print(method)
            print(method.code)
            for c in method.code.disassemble():
                print(c)

            print()
