from pyjvm import actions
from pyjvm.actions import IncrementProgramCounter
from pyjvm.instructions.instructions import Instructor, bytecode
from pyjvm.jvm_types import CompType


# noinspection PyAbstractClass
class StackInstructor(Instructor):
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


@bytecode('dup')
class Duplicate(Instructor):
    def execute(self):
        return IncrementProgramCounter.after(
            actions.Push(self.peek_op_stack())
        )


@bytecode('dup_x1')
class DuplicateX1(Instructor):
    def execute(self):
        top = self.peek_op_stack()
        ante_top = self.peek_op_stack(1)
        return IncrementProgramCounter.after(
            actions.Pop(2),
            actions.PushMany([
                top, ante_top, top
            ])
        )


@bytecode('dup_x2')
class DuplicateX2(StackInstructor):
    def execute(self):
        if self.matches_comp_types('111'):
            first, second, third = self.peek_many(3)
            ops = [
                actions.Pop(3),
                actions.PushMany([
                    first, second, third, first
                ])
            ]
        elif self.matches_comp_types('12'):
            first, second = self.peek_many(2)
            ops = [
                actions.Pop(2),
                actions.PushMany([
                    first, second, first
                ])
            ]
        else:
            raise ValueError('No comp type case match')

        return IncrementProgramCounter.after(*ops)
