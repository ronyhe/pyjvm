from pyjvm.actions import Pop, Push, GoTo
from pyjvm.instructions.comparisons import BOOLEAN_COMPARISONS, UNARY_BRANCH_COMPARISONS, BINARY_BRANCH_COMPARISONS, \
    BINARY_REFERENCE_COMPARISONS
from pyjvm.jvm_types import Integer
from pyjvm.utils import bool_to_num
from test.utils import assert_incrementing_instruction, assert_instruction, literal_instruction, DUMMY_CLASS, \
    dummy_loader


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


def _test_branch_comp(name, source, offset, values, type_, op):
    try:
        values = list(values)
    except TypeError:
        values = [values]

    result = op(*values)
    if result:
        actual_offset = offset
    else:
        actual_offset = 1
    target = source + actual_offset

    # noinspection PyProtectedMember
    assert_instruction(
        instruction=literal_instruction(name, offset)._replace(pos=source),
        op_stack=[type_.create_instance(v) for v in values],
        expected=[
            Pop(len(values)),
            GoTo(target)
        ]
    )


def test_binary_branch_comparisons():
    offset = 6
    source = 3

    values = 4, 5
    for name, op in BINARY_BRANCH_COMPARISONS.items():
        _test_branch_comp(name, source, offset, values, Integer, op)


def test_unary_branch_comparisons():
    value = 22
    offset = 5
    source = 2

    for name, op in UNARY_BRANCH_COMPARISONS.items():
        _test_branch_comp(name, source, offset, value, Integer, lambda v: op(v, 0))


def test_reference_binary_branch_comparisons():
    offset = 7
    source = 4
    instance = dummy_loader().default_instance(DUMMY_CLASS.name)
    values = [instance, instance]

    for name, op in BINARY_REFERENCE_COMPARISONS.items():
        _test_branch_comp(name, source, offset, values, DUMMY_CLASS.type, op)
