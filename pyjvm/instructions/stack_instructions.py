from pyjvm.core import actions
from pyjvm.core.actions import IncrementProgramCounter
from pyjvm.core.jvm_types import CompType
from pyjvm.instructions.instructions import Instructor, bytecode, bytecode_dict


def _single_iterable_byte_code_dict(specs):
    return bytecode_dict({k: [v] for k, v in specs.items()})


@_single_iterable_byte_code_dict({
    'dup': [
        ('1', 1, 1)
    ],
    'dup_x1': [
        ('1', 1, 2),
        ('2', 1, 2)
    ],
    'dup_x2': [
        ('111', 1, 3),
        ('12', 1, 2)
    ],
    'dup2': [
        ('11', 2, 2),
        ('2', 1, 1)
    ],
    'dup2_x1': [
        ('111', 2, 3),
        ('21', 1, 2)
    ],
    'dup2_x2': [
        ('1111', 2, 4),
        ('211', 1, 3),
        ('112', 2, 3),
        ('22', 1, 2)
    ]
})
class DuplicationInstructor(Instructor):
    """Duplicate a certain amount of values from the top of the stack

    The exact behaviour of these instructions differ according to the values on the stack.
    More specifically the so called computational type of those values (see section 2.11.1 of the JVM 8 spec).

    To avoid repetition, this Instructor takes a `specs` argument which is an iterable.
    Each spec is a 3-tuple:
        - A string of '1's and '2's, indicating whether the value at that stack position should be comp type 1 or 2
          The top of the stack is on the left of this string
        - The amount of values to duplicate from the top if the string matches the current situation
        - An offset from the top at which the duplicated items should be inserted

    These specs will be checked in order and if one matches - it will execute.
    If none match a ValueError will be raised.

    For example, the spec `('11', 1, 2)` does not match this stack:
        - Long 0 (top)
        - Integer 1
        - ... rest of stack
    Because Long is of computational type 2.
    However this spec `('21', 1, 2)` does match, and will produce the following stack:
        - Long 0 (top)
        - Integer 1
        - Long 0
        - Integer 1
        - ... rest of stack

    """

    def __init__(self, inputs, specs):
        super().__init__(inputs)
        self.specs = list(specs)

    def execute(self):
        for comp_type_string, amount_to_take, index_for_insertion in self.specs:
            if self.matches_comp_types(comp_type_string):
                return IncrementProgramCounter.after(
                    actions.DuplicateTop(amount_to_take=amount_to_take, index_for_insertion=index_for_insertion)
                )

        raise ValueError('No comp type case match')

    def matches_comp_types(self, numbers):
        numbers = [int(i) for i in numbers]
        for index, num in enumerate(numbers):
            try:
                stack_value = self.peek_op_stack(index)
                comp = CompType(stack_value)
            except (TypeError, IndexError):
                return False
            bool_value = comp.is_one if num == 1 else comp.is_two
            if not bool_value:
                return False

        return True


@bytecode('pop', 1)
@bytecode('pop2', 2)
class Pop(Instructor):
    """Pops `amount` of values from top-of-stack"""

    def __init__(self, inputs, amount):
        super().__init__(inputs)
        self.amount = amount

    def execute(self):
        return IncrementProgramCounter.after(
            actions.Pop(self.amount)
        )


@bytecode('swap')
class Swap(Instructor):
    """Swaps top-of-stack with the value directly beneath it"""

    def execute(self):
        return IncrementProgramCounter.after(
            actions.Pop(2),
            actions.Push(self.peek_op_stack(0)),
            actions.Push(self.peek_op_stack(1))
        )
