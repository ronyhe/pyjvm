"""
Instructors for comparison instructions


"""
import operator

from pyjvm import actions
from pyjvm.actions import IncrementProgramCounter, Actions
from pyjvm.instructions.instructions import bytecode_dict, Instructor, bytecode
from pyjvm.utils.utils import bool_to_num

# Comparisons that push a boolean result
# noinspection SpellCheckingInspection
BOOLEAN_COMPARISONS = {
    'lcmp': operator.eq,
    'fcmpl': operator.le,
    'fcmpg': operator.ge,
    'dcmpl': operator.le,
    'dcmpg': operator.ge,
}

# Comparisons that compare to zero and branch if True
# noinspection SpellCheckingInspection
UNARY_BRANCH_COMPARISONS = {
    'ifeq': operator.eq,
    'ifne': operator.ne,
    'iflt': operator.lt,
    'ifge': operator.ge,
    'ifgt': operator.gt,
    'ifle': operator.le
}

# Comparisons that branch if True
# noinspection SpellCheckingInspection
BINARY_BRANCH_COMPARISONS = {
    "if_icmpeq": operator.eq,
    "if_icmpne": operator.ne,
    "if_icmplt": operator.lt,
    "if_icmpge": operator.ge,
    "if_icmpgt": operator.gt,
    "if_icmple": operator.le,
}

# Reference assertions that branch if True
# noinspection SpellCheckingInspection
BINARY_REFERENCE_COMPARISONS = {
    "if_acmpeq": operator.is_,
    "if_acmpne": operator.is_not
}


def unary_op(op):
    """Return an operator that uses 0 as its second argument"""
    return lambda n: op(n, 0)


def _dict_to_instruction_dict(d):
    # bytecode_dict expected a list of arguments
    return {k: [v] for k, v in d.items()}


def _create_instruction_dict_for_branch_comparisons():
    """Convert the instructions into the format that `BranchComparison` expects"""
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


@bytecode_dict(_create_instruction_dict_for_branch_comparisons())
class BranchComparison(Instructor):
    """ An instructor for branching comparisons

    It pops the values and sends them to the provided `op`.
    If the `op` returns True it jumps to the target offset.
    If not it still jumps, but to the next instruction, which is exacyly like not jumping.
    """

    def __init__(self, inputs, pops, op):
        """Return a `BranchComparison` instance

        :param inputs: An `InstructorInputs` instance
        :param pops: The amount of value to pop
        :param op: A function that will get the values and return bool
        """
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
        # Here we return the popped instance.
        # So, `v` instead of `v.value`
        # That way the op has access to the `is_null` method.
        return [v for v in self.peek_many(self.pops)]


@bytecode_dict(_dict_to_instruction_dict(BOOLEAN_COMPARISONS))
class BooleanComparison(Instructor):
    """An instructor for boolean comparisons

    It pops the values and sends them to the provided `op`.
    If the result is True it pushes the Integer 1
    Else it pushes the Integer 0
    """

    def __init__(self, inputs, op):
        super().__init__(inputs)
        # A function that will get the values and return bool
        self.op = op

    def execute(self):
        values = (value.value for value in self.peek_many(2))
        bool_result = self.op(*values)
        num_result = bool_to_num(bool_result)
        return IncrementProgramCounter.after(
            actions.Pop(2),
            actions.Push(num_result)
        )
