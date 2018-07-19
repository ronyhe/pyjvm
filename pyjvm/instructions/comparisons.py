import operator

from pyjvm import actions
from pyjvm.actions import IncrementProgramCounter, Actions
from pyjvm.instructions.instructions import bytecode_dict, Instructor

# noinspection SpellCheckingInspection
from pyjvm.utils import bool_to_num

BOOLEAN_COMPARISONS = {
    'lcmp': operator.eq,
    'fcmpl': operator.le,
    'fcmpg': operator.ge,
    'dcmpl': operator.le,
    'dcmpg': operator.ge,
}
_BOOLEAN_INSTRUCTION_DICT = {k: [v] for k, v in BOOLEAN_COMPARISONS.items()}

# noinspection SpellCheckingInspection
UNARY_BRANCH_COMPARISONS = {
    'ifeq': operator.eq,
    'ifne': operator.ne,
    'iflt': operator.lt,
    'ifge': operator.ge,
    'ifgt': operator.gt,
    'ifle': operator.le
}
_UNARY_BRANCH_COMPARISON_DICT = {k: [v] for k, v in UNARY_BRANCH_COMPARISONS.items()}


@bytecode_dict(_BOOLEAN_INSTRUCTION_DICT)
class BooleanComparison(Instructor):
    def __init__(self, inputs, op):
        super().__init__(inputs)
        self.op = op

    def execute(self):
        values = (value.value for value in self.peek_many(2))
        bool_result = self.op(*values)
        num_result = bool_to_num(bool_result)
        return IncrementProgramCounter.after(
            actions.Pop(2),
            actions.Push(num_result)
        )


@bytecode_dict(_UNARY_BRANCH_COMPARISON_DICT)
class UnaryBranchComparison(Instructor):
    def __init__(self, inputs, op):
        super().__init__(inputs)
        self.op = op

    def execute(self):
        value = self.peek_op_stack()

        result = self.op(value.value, 0)
        if result:
            offset = self.operand_as_int()
        else:
            offset = 1

        source = self.instruction.pos
        target = source + offset

        return Actions(
            actions.Pop(),
            actions.GoTo(target)
        )
