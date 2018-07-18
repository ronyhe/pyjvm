from pyjvm.actions import ReturnResult
from pyjvm.instructions.control import RETURN_RESULT_INSTRUCTIONS
from pyjvm.jvm_types import Integer
from test.utils import assert_instruction


def test_return_results():
    value = Integer.create_instance(5)

    for instruction in RETURN_RESULT_INSTRUCTIONS:
        assert_instruction(
            instruction=instruction,

            op_stack=[value],

            expected=[
                ReturnResult(value)
            ]
        )
