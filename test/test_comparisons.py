from pyjvm.actions import Pop, Push, GoTo
from pyjvm.instructions.comparisons import BOOLEAN_COMPARISONS, UNARY_BRANCH_COMPARISONS, BINARY_BRANCH_COMPARISONS
from pyjvm.jvm_types import Integer
from pyjvm.utils import bool_to_num
from test.utils import assert_incrementing_instruction, assert_instruction, literal_instruction


def test_comparisons():
    values = 43, 23
    for name, op in BOOLEAN_COMPARISONS.items():
        assert_incrementing_instruction(
            instruction=name,
            op_stack=[*(Integer.create_instance(v) for v in values)],
            expected=[
                Pop(2),
                Push(bool_to_num(op(*values)))
            ]
        )


def test_unary_branch_comparisons():
    value = 22
    offset = 5
    source = 2

    for name, op in UNARY_BRANCH_COMPARISONS.items():
        # noinspection PyProtectedMember
        instruction = literal_instruction(name, offset)._replace(pos=source)

        result = op(value, 0)
        if result:
            target = source + offset
        else:
            target = source + 1

        assert_instruction(
            instruction=instruction,
            op_stack=[Integer.create_instance(value)],
            expected=[Pop(), GoTo(target)]
        )


def test_binary_branch_comparisons():
    offset = 6
    source = 3

    values = 4, 5
    for name, op in BINARY_BRANCH_COMPARISONS.items():
        # noinspection PyProtectedMember
        instruction = literal_instruction(name, offset)._replace(pos=source)
        result = op(*values)
        if result:
            target = source + offset
        else:
            target = source + 1

        assert_instruction(
            instruction=instruction,
            op_stack = [Integer.create_instance(v) for v in values],
            expected=[
                Pop(2),
                GoTo(target)
            ]
        )
