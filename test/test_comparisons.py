from pyjvm.actions import Pop, Push
from pyjvm.instructions.comparisons import BOOLEAN_COMPARISONS
from pyjvm.jvm_types import Integer
from pyjvm.utils import bool_to_num
from test.utils import assert_incrementing_instruction


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
