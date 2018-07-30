from pyjvm.core.actions import Push, Pop
from pyjvm.instructions.conversions import CONVERSION_DICT
from test.utils import assert_incrementing_instruction


def test_conversions():
    for name, types in CONVERSION_DICT.items():
        source, target = types
        value = 3
        assert_incrementing_instruction(
            instruction=name,

            op_stack=[source.create_instance(value)],

            expected=[
                Pop(),
                Push(target.create_instance(value))
            ]
        )
