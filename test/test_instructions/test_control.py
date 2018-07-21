from pyjvm.actions import ReturnResult, ReturnVoid, GoTo, Pop
from pyjvm.instructions.control import RETURN_RESULT_INSTRUCTIONS
from pyjvm.instructions.switches import LookupSwitch, TableSwitch
from pyjvm.model.jvm_types import Integer
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
    offset = 4
    source = 10
    # noinspection PyProtectedMember
    instruction = literal_instruction('goto', offset)._replace(pos=source)
    target = offset + source

    assert_instruction(
        instruction=instruction,
        expected=[
            GoTo(target)
        ]
    )


def test_lookup_switch():
    source = 1
    switch = LookupSwitch(10, [
        (0, 3),
        (1, 6),
        (2, 9)
    ])
    irrelevant_value = max(switch.pairs.values()) + 1
    instruction = switch.create_instruction(source)

    for value, offset in switch.pairs.items():
        assert_instruction(
            instruction=instruction,
            op_stack=[Integer.create_instance(value)],
            expected=[
                Pop(),
                GoTo(source + offset)
            ]
        )

    assert_instruction(
        instruction=instruction,
        op_stack=[Integer.create_instance(irrelevant_value)],
        expected=[
            Pop(),
            GoTo(source + switch.default)
        ]
    )


def test_table_switch():
    source = 1
    switch = TableSwitch(10, [2, 3, 4])
    instruction = switch.create_instruction(source)
    irrelevant_value = switch.high * 2

    for i, off in enumerate(switch.offsets):
        assert_instruction(
            instruction=instruction,
            op_stack=[Integer.create_instance(i + switch.low)],
            expected=[
                Pop(),
                GoTo(source + off)
            ]
        )

    assert_instruction(
        instruction=instruction,
        op_stack=[Integer.create_instance(irrelevant_value)],
        expected=[
            Pop(),
            GoTo(source + switch.default)
        ]
    )
