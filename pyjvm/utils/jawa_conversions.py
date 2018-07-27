"""Function for converting from instance of types from the jawa library to pyjvm runtime types"""
from typing import Iterable

import jawa.methods
import jawa.util.descriptor
from jawa import constants
from jawa.cf import ClassFile
from jawa.methods import Method

from pyjvm.model.jvm_class import JvmClass, BytecodeMethod, MethodKey, JvmObject
from pyjvm.model.jvm_types import Type, Integer, Float, Long, Double, ArrayReferenceType, ObjectReferenceType, \
    RootObjectType
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


def _convert_methods_to_mapping(jawa_methods: Iterable[Method]):
    def convert(method: Method):
        return key_from_method(method), convert_method(method)

    return [convert(m) for m in jawa_methods]


def convert_class_file(cf: ClassFile) -> JvmClass:
    """Convert a ClassFile to a JvmClass"""
    static_fields, instance_fields = split_by_predicate(cf.fields, lambda f: f.access_flags.get('acc_static'))
    static_fields = _fields_to_pairs(static_fields)
    instance_fields = _fields_to_pairs(instance_fields)

    class_name = cf.this.name.value
    is_root = class_name == RootObjectType.refers_to
    if is_root:
        parent_name = None
    else:
        parent_name = cf.super_.name.value

    return JvmClass(
        class_name,
        parent_name,
        cf.constants,
        (face.name.value for face in cf.interfaces),
        instance_fields,
        _convert_methods_to_mapping(cf.methods),
        static_fields
    )


def key_from_method(method):
    """Extract a MethodKey from a jawa method"""
    return MethodKey(method.name.value, method.descriptor.value)


def key_from_method_ref(ref):
    """Extract a MethodKey from a jawa method reference constant"""
    name = ref.name_and_type.name.value
    descriptor = ref.name_and_type.descriptor.value
    return MethodKey(name, descriptor)


def convert_method(method: jawa.methods.Method) -> BytecodeMethod:
    """Convert a jawa method to a BytecodeMethod"""
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
    """Convert a jawa JvmType to a Type"""
    return _convert_type(*type_)


def _convert_const_to_string_instance(const):
    text = const.string.value
    chars = [ord(c) for c in text]
    char_array = ArrayReferenceType(Integer).create_instance(chars)
    hash_value = hash(text) % (2 ** 32)
    hash_ = Integer.create_instance(hash_value)
    ref_type = ObjectReferenceType('java/lang/String')
    return ref_type.create_instance(JvmObject({
        'hash': hash_,
        'value': char_array
    }))


def convert_constant(const):
    """Convert a jawa constant from a ConstantPool to a JvmValue"""
    const_type = type(const)

    if const_type == jawa.constants.String:
        return _convert_const_to_string_instance(const)

    types = {
        constants.Integer: Integer,
        constants.Float: Float,
        constants.Long: Long,
        constants.Double: Double,
    }

    jvm_type = types[const_type]
    return jvm_type.create_instance(const.value)


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
