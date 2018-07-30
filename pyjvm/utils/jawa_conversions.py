"""Functions for converting from jawa library types to pyjvm runtime types

The jawa library provides the parsing part of pyjvm, so there's a need to 'translate' the
data structures after parsing.

However, there was no need to pedantically recreate all that jawa did. Some of their structures were a great fit:
 - The Instruction class
 - The ConstantPool class and its supportive structures
"""
from typing import Iterable

import jawa.methods
import jawa.util.descriptor
from jawa import constants as jawa_constants
from jawa.cf import ClassFile
from jawa.methods import Method

from pyjvm.core.jvm_class import JvmClass, BytecodeMethod, MethodKey, JvmObject, Handlers, ExceptionHandler
from pyjvm.core.jvm_types import Type, Integer, Float, Long, Double, ArrayReferenceType, ObjectReferenceType, \
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


def convert_class_file(cf: ClassFile) -> JvmClass:
    """Convert a ClassFile to a JvmClass"""
    static_fields, instance_fields = split_by_predicate(cf.fields, _is_static_field)
    static_fields = _fields_to_pairs(static_fields)
    instance_fields = _fields_to_pairs(instance_fields)
    class_name = cf.this.name.value

    return JvmClass(
        name=class_name,
        name_of_base=_name_of_base(cf, class_name),
        constants=cf.constants,
        interfaces=(face.name.value for face in cf.interfaces),
        fields=instance_fields,
        methods=_convert_methods_to_mapping(cf.methods, cf.constants),
        static_fields=static_fields
    )


def key_from_method(method):
    """Extract a MethodKey from a jawa method"""
    return MethodKey(method.name.value, method.descriptor.value)


def key_from_method_ref(ref):
    """Extract a MethodKey from a jawa method reference constant"""
    name = ref.name_and_type.name.value
    descriptor = ref.name_and_type.descriptor.value
    return MethodKey(name, descriptor)


def convert_method(method: jawa.methods.Method, constants) -> BytecodeMethod:
    """Convert a jawa method to a BytecodeMethod"""
    name = method.name.value
    descriptor = method.descriptor.value
    arg_types = [convert_type(t) for t in method.args]
    is_native = method.access_flags.get('acc_native')
    code = method.code
    handlers = _create_exception_handlers(code, constants)
    instructions, max_locals, max_stack = _instructions_locals_stack(code)

    return BytecodeMethod(
        name=name,
        descriptor=descriptor,
        instructions=instructions,
        args=arg_types,
        max_locals=max_locals,
        max_stack=max_stack,
        is_native=is_native,
        exception_handlers=handlers
    )


def convert_type(type_: jawa.util.descriptor.JVMType) -> Type:
    """Convert a jawa JvmType to a Type"""
    return _convert_type(*type_)


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
        return ObjectReferenceType(name)
    else:
        return _LETTERS_MAP[base.upper()]


def _field_to_pair(field):
    return field.name.value, convert_type(field.type)


def _fields_to_pairs(fields):
    return [_field_to_pair(f) for f in fields]


def _convert_methods_to_mapping(jawa_methods: Iterable[Method], constants):
    def convert(method: Method):
        return key_from_method(method), convert_method(method, constants)

    return [convert(m) for m in jawa_methods]


def _is_static_field(field):
    return bool(field.access_flags.get('acc_static'))


def _name_of_base(cf: ClassFile, class_name):
    is_root = class_name == RootObjectType.refers_to
    if is_root:
        parent_name = None
    else:
        parent_name = cf.super_.name.value

    return parent_name


def _create_exception_handler(table_entry, constants):
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


def _create_exception_handlers(code, constants):
    if code is None or code.exception_table is None:
        handlers = []
    else:
        handlers = [_create_exception_handler(ex, constants) for ex in code.exception_table]

    return Handlers(handlers)


def _instructions_locals_stack(code):
    if code is None:
        return [], 0, 0
    else:
        return code.disassemble(), code.max_locals, code.max_stack


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
