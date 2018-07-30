from jawa.constants import ConstantPool
from jawa.util.bytecode import Instruction

from pyjvm.core.actions import Pop, Invoke
from pyjvm.core.class_loaders import FixedClassLoader
from pyjvm.core.jvm_class import JvmClass, BytecodeMethod, MethodKey
from pyjvm.core.jvm_types import Integer, RootObjectType
from test.utils import constant_instruction, assert_instruction, SOME_INT


def test_invoke_v():
    method_name = 'method_name'
    class_name = 'class_name'

    consts = ConstantPool()
    descriptor = '(II)V'
    key = MethodKey(method_name, descriptor)
    no_op = Instruction.create('nop')

    method = BytecodeMethod(
        name='method_name',
        descriptor='(II)V',
        max_locals=5,
        max_stack=5,
        instructions=[no_op, no_op],
        args=[Integer, Integer],
    )

    jvm_class = JvmClass(
        class_name,
        RootObjectType.refers_to,
        consts,
        methods={
            key: method
        }
    )

    method_ref = consts.create_method_ref(class_name, method_name, descriptor)
    instruction = constant_instruction('invokevirtual', method_ref)
    loader = FixedClassLoader({
        class_name: jvm_class
    })

    instance = loader.default_instance(class_name)
    arg_value = SOME_INT
    arguments = [instance, arg_value, arg_value]
    reversed_arguments = list(reversed(arguments))
    assert_instruction(
        constants=consts,
        loader=loader,
        instruction=instruction,
        op_stack=reversed_arguments,
        expected=[
            Pop(3),
            Invoke(class_name, key, arguments)
        ]
    )
