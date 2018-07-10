from pyjvm import actions
from pyjvm.actions import IncrementProgramCounter
from pyjvm.instructions.instructions import Instructor, bytecode, bytecode_dict
from pyjvm.jvm_types import CompType


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
    ]
})
class DuplicationInstructor(Instructor):
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
    def __init__(self, inputs, amount):
        super().__init__(inputs)
        self.amount = amount

    def execute(self):
        return IncrementProgramCounter.after(
            actions.Pop(self.amount)
        )
