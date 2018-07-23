import jawa.methods
import jawa.util.descriptor
from jawa import constants
from jawa.cf import ClassFile

from pyjvm.model.jvm_class import JvmClass, BytecodeMethod
from pyjvm.model.jvm_types import Type, Integer, Float, Long, Double, ArrayReferenceType, ObjectReferenceType
from pyjvm.utils.utils import split_by_predicate

_LETTERS_MAP = {
    'D': Double,
    'F': Float,
    'J': Long,
    'B': Integer,
    'C': Integer,
    'I': Integer,
    'Z': Integer
}


def _field_to_pair(field):
    return field.name.value, convert_type(field.type)


def _fields_to_pairs(fields):
    return [_field_to_pair(f) for f in fields]


def convert_class_file(cf: ClassFile) -> JvmClass:
    static_fields, instance_fields = split_by_predicate(cf.fields, lambda f: f.access_flags.get('acc_static'))
    static_fields = _fields_to_pairs(static_fields)
    instance_fields = _fields_to_pairs(instance_fields)

    return JvmClass(
        cf.this.name.value,
        cf.super_.name.value,
        cf.constants,
        (face.name.value for face in cf.interfaces),
        instance_fields,
        ((method.name.value, convert_method(method)) for method in cf.methods),
        static_fields
    )


def convert_method(method: jawa.methods.Method) -> BytecodeMethod:
    arg_types = [convert_type(t) for t in method.args]
    if method.code is not None:
        return BytecodeMethod(
            method.code.max_locals,
            method.code.max_stack,
            method.code.disassemble(),
            arg_types,
            name=method.name.value
        )
    else:
        return BytecodeMethod(
            0,
            0,
            [],
            arg_types,
            name=method.name.value
        )


def convert_type(type_: jawa.util.descriptor.JVMType) -> Type:
    return _convert_type(*type_)


def convert_constant(const):
    types = {
        constants.Integer: Integer,
        constants.Float: Float,
        constants.Long: Long,
        constants.Double: Double,
    }
    type_ = types[type(const)]
    return type_.create_instance(const.value)


def _convert_type(base, dimensions, name):
    if dimensions > 0:
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
