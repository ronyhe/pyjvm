from jawa.constants import ConstantPool

from pyjvm.actions import Pop, Invoke
from pyjvm.model.jvm_types import Integer
from test.utils import DUMMY_CLASS, assert_incrementing_instruction, constant_instruction, dummy_loader


def test_invoke_virtual():
    method_name = DUMMY_CLASS.method.name.value
    loader = dummy_loader()

    consts = ConstantPool()
    method_ref = DUMMY_CLASS.method_ref(consts)

    class_name = DUMMY_CLASS.name
    instance = loader.default_instance(class_name)

    argument = Integer.create_instance(31)

    assert_incrementing_instruction(
        constants=consts,
        instruction=constant_instruction('invokevirtual', method_ref),
        op_stack=[instance, argument],
        expected=[
            Pop(2),
            Invoke(class_name, method_name, [instance, argument])
        ]
    )
