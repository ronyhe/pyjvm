import operator

from pyjvm import actions
from pyjvm.actions import IncrementProgramCounter, Actions
from pyjvm.instructions.instructions import bytecode_dict, Instructor
from pyjvm.utils import bool_to_num


def _dict_to_instruction_dict(d):
    return {k: [v] for k, v in d.items()}


# noinspection SpellCheckingInspection
BOOLEAN_COMPARISONS = {
    'lcmp': operator.eq,
    'fcmpl': operator.le,
    'fcmpg': operator.ge,
    'dcmpl': operator.le,
    'dcmpg': operator.ge,
}

# noinspection SpellCheckingInspection
UNARY_BRANCH_COMPARISONS = {
    'ifeq': operator.eq,
    'ifne': operator.ne,
    'iflt': operator.lt,
    'ifge': operator.ge,
    'ifgt': operator.gt,
    'ifle': operator.le
}

# noinspection SpellCheckingInspection
BINARY_BRANCH_COMPARISONS = {
    "if_icmpeq": operator.eq,
    "if_icmpne": operator.ne,
    "if_icmplt": operator.lt,
    "if_icmpge": operator.ge,
    "if_icmpgt": operator.gt,
    "if_icmple": operator.le,
}

# noinspection SpellCheckingInspection
BINARY_REFERENCE_COMPARISONS = {
    "if_acmpeq": operator.is_,
    "if_acmpne": operator.is_not
}


@bytecode_dict(_dict_to_instruction_dict(BOOLEAN_COMPARISONS))
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


@bytecode_dict(_dict_to_instruction_dict(UNARY_BRANCH_COMPARISONS))
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


@bytecode_dict(_dict_to_instruction_dict(BINARY_BRANCH_COMPARISONS))
@bytecode_dict(_dict_to_instruction_dict(BINARY_REFERENCE_COMPARISONS))
class BinaryBranchComparison(Instructor):
    def __init__(self, inputs, op):
        super().__init__(inputs)
        self.op = op

    def execute(self):
        values = self.peek_many(2)

        result = self.op(*(value.value for value in values))
        if result:
            offset = self.operand_as_int()
        else:
            offset = 1

        source = self.instruction.pos
        target = source + offset

        return Actions(
            actions.Pop(2),
            actions.GoTo(target)
        )
