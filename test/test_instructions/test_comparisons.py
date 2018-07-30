from pyjvm.core.actions import Pop, Push, GoTo
from pyjvm.core.jvm_types import Integer, NULL_OBJECT, ArrayReferenceType, ObjectReferenceType
from pyjvm.instructions.comparisons import BOOLEAN_COMPARISONS, UNARY_BRANCH_COMPARISONS, BINARY_BRANCH_COMPARISONS, \
    BINARY_REFERENCE_COMPARISONS, unary_op
from pyjvm.utils.utils import bool_to_num, named_tuple_replace
from test.utils import assert_incrementing_instruction, assert_instruction, literal_instruction, NPE_CLASS_NAME


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
    result = op(*values)
    if result:
        actual_offset = offset
    else:
        actual_offset = 1
    target = source + actual_offset

    instruction = literal_instruction(name, offset)
    instruction = named_tuple_replace(instruction, pos=source)
    try:
        assert_instruction(
            instruction=instruction,
            op_stack=[type_.create_instance(v) for v in values],
            expected=[
                Pop(len(values)),
                GoTo(target)
            ]
        )
    except AssertionError as e:
        raise AssertionError(f'Branch comparison test for {name} failed') from e


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
        _test_branch_comp(name, source, offset, [value], Integer, unary_op(op))


def test_reference_binary_branch_comparisons(std_loader):
    offset = 7
    source = 4

    npe = NPE_CLASS_NAME
    instance = std_loader.default_instance(npe).value
    values = [instance, instance]

    for name, op in BINARY_REFERENCE_COMPARISONS.items():
        _test_branch_comp(name, source, offset, values, ObjectReferenceType(npe), op)


def test_if_null():
    offset = 10
    source = 3
    value = ArrayReferenceType(Integer).create_instance(NULL_OBJECT)

    instruction = literal_instruction('ifnull', offset)
    instruction = named_tuple_replace(instruction, pos=source)
    assert_instruction(
        instruction=instruction,
        op_stack=[value],
        expected=[
            Pop(),
            GoTo(source + offset)
        ]
    )
