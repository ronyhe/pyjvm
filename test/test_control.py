from pyjvm.actions import ReturnResult, ReturnVoid, GoTo
from pyjvm.instructions.control import RETURN_RESULT_INSTRUCTIONS
from pyjvm.jvm_types import Integer
from test.utils import assert_instruction, literal_instruction


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


def test_return_void():
    assert_instruction(
        instruction='return',
        expected=[ReturnVoid()]
    )


def test_go_to():
    # noinspection PyProtectedMember
    offset = 4
    source = 10
    instruction = literal_instruction('goto', offset)._replace(pos=source)
    target = offset + source

    assert_instruction(
        instruction=instruction,
        expected=[
            GoTo(target)
        ]
    )
