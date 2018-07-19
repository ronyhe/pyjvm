import operator

from pyjvm import actions
from pyjvm.actions import IncrementProgramCounter
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
