from jawa.constants import ConstantPool

from pyjvm.actions import Pop, Invoke
from pyjvm.model.jvm_types import Integer
from pyjvm.utils.jawa_conversions import key_from_method
from test.utils import DUMMY_CLASS, constant_instruction, dummy_loader, \
    assert_instruction


def test_invoke_virtual():
    key = key_from_method(DUMMY_CLASS.method)
    loader = dummy_loader()

    consts = ConstantPool()
    method_ref = DUMMY_CLASS.method_ref(consts)

    class_name = DUMMY_CLASS.name
    instance = loader.default_instance(class_name)

    argument = Integer.create_instance(31)

    assert_instruction(
        constants=consts,
        instruction=constant_instruction('invokevirtual', method_ref),
        op_stack=[instance, argument],
        expected=[
            Pop(2),
            Invoke(class_name, key, [instance, argument])
        ]
    )
