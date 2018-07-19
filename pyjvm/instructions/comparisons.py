import operator

from pyjvm import actions
from pyjvm.actions import IncrementProgramCounter, Actions
from pyjvm.instructions.instructions import bytecode_dict, Instructor, bytecode
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


def unary_op(op):
    return lambda n: op(n, 0)


def _create_instruction_dict():
    dic = {}
    dic.update({
        k: [1, unary_op(v)] for k, v in UNARY_BRANCH_COMPARISONS.items()
    })
    dic.update({
        k: [2, v] for k, v in BINARY_BRANCH_COMPARISONS.items()
    })
    dic.update({
        k: [2, v] for k, v in BINARY_REFERENCE_COMPARISONS.items()
    })

    return dic


@bytecode_dict(_create_instruction_dict())
class BranchComparison(Instructor):
    def __init__(self, inputs, pops, op):
        super().__init__(inputs)
        self.pops = pops
        self.op = op

    def execute(self):
        values = self._get_values()
        result = self.op(*values)

        if result:
            offset = self.operand_as_int()
        else:
            offset = 1

        target = self.instruction.pos + offset
        return Actions(
            actions.Pop(self.pops),
            actions.GoTo(target)
        )

    def _get_values(self):
        return [v.value for v in self.peek_many(self.pops)]


@bytecode('ifnull', 1, lambda v: v.is_null)
@bytecode('ifnonnull', 1, lambda v: not v.is_null)
class NullBranchComparison(BranchComparison):
    def _get_values(self):
        return [v for v in self.peek_many(self.pops)]


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
