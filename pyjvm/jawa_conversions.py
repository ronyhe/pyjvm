import jawa.methods
import jawa.util.descriptor
from jawa.cf import ClassFile

from pyjvm.jvm_class import JvmClass, BytecodeMethod
from pyjvm.jvm_types import Type, Integer, Float, Long, Double, ArrayReferenceType, ObjectReferenceType

_LETTERS_MAP = {
    'D': Double,
    'F': Float,
    'J': Long,
    'B': Integer,
    'C': Integer,
    'I': Integer,
    'Z': Integer
}


def convert_class_file(cf: ClassFile) -> JvmClass:
    return JvmClass(
        cf.this.name.value,
        cf.super_.name.value,
        cf.constants,
        (face.name.value for face in cf.interfaces),
        ((field.name.value, convert_type(field.type)) for field in cf.fields),
        ((method.name.value, convert_method(method)) for method in cf.methods)
    )


def convert_method(method: jawa.methods.Method) -> BytecodeMethod:
    return BytecodeMethod(
        method.code.max_locals,
        method.code.max_stack,
        method.code.disassemble()
    )


def convert_type(type_: jawa.util.descriptor.JVMType) -> Type:
    return _convert_type(*type_)


def _convert_type(base, dimensions, name):
    if dimensions > 1:
        return ArrayReferenceType(_convert_type(base, dimensions - 1, name))
    else:
        return _atom_type(base, name)


def _atom_type(base, name):
    if base == 'L':
        return _class(name)
    else:
        return _LETTERS_MAP[base.upper()]


def _class(name):
    return ObjectReferenceType(name)
