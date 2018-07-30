"""Function for converting from instance of types from the jawa library to pyjvm runtime types"""
from typing import Iterable

import jawa.methods
import jawa.util.descriptor
from jawa import constants as jawa_constants
from jawa.cf import ClassFile
from jawa.methods import Method

from pyjvm.model.jvm_class import JvmClass, BytecodeMethod, MethodKey, JvmObject, Handlers, ExceptionHandler
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


def _convert_methods_to_mapping(jawa_methods: Iterable[Method], constants):
    def convert(method: Method):
        return key_from_method(method), convert_method(method, constants)

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
        _convert_methods_to_mapping(cf.methods, cf.constants),
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


def _create_handler(table_entry, constants):
    start, end, handler, type_index = table_entry
    if type_index == 0:
        # This is an explicit exception to the rule, as stated in the spec.
        # See JVM 8 specification section 4.7.3
        name = RootObjectType.refers_to
    else:
        type_constant = constants[type_index]
        name = type_constant.name.value
    handler = ExceptionHandler(start, end, handler, name)
    return handler


def convert_method(method: jawa.methods.Method, constants) -> BytecodeMethod:
    """Convert a jawa method to a BytecodeMethod"""
    arg_types = [convert_type(t) for t in method.args]
    is_native = method.access_flags.get('acc_native')

    code = method.code
    if code is not None:
        if code.exception_table is None:
            handlers = Handlers()
        else:
            handlers = Handlers([_create_handler(ex, constants) for ex in code.exception_table])

        return BytecodeMethod(
            code.max_locals,
            code.max_stack,
            code.disassemble(),
            arg_types,
            name=method.name.value,
            descriptor=method.descriptor.value,
            is_native=is_native,
            exception_handlers=handlers
        )
    else:
        return BytecodeMethod(
            0,
            0,
            [],
            arg_types,
            name=method.name.value,
            is_native=is_native
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

    if const_type == jawa_constants.String:
        return _convert_const_to_string_instance(const)

    types = {
        jawa_constants.Integer: Integer,
        jawa_constants.Float: Float,
        jawa_constants.Long: Long,
        jawa_constants.Double: Double,
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
