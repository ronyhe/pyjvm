from pyjvm.instructions.instructions import Executor, bytecode
from pyjvm.jvm_types import CompType


@bytecode('pop', 1)
@bytecode('pop2', 2)
class Pop(Executor):
    def __init__(self, instruction, machine, amount):
        super().__init__(instruction, machine)
        self.amount = amount

    def execute(self):
        for _ in range(self.amount):
            self.machine.current_op_stack().pop()


@bytecode('dup', 0)
@bytecode('dup_x1', 2)
class Duplicate(Executor):
    def __init__(self, instruction, machine, insertion_off_set_from_top):
        super().__init__(instruction, machine)
        self.insertion_off_set_from_top = insertion_off_set_from_top

    def execute(self):
        value = self.machine.current_op_stack().peek().duplicate()
        self.machine.current_op_stack().insert_at_offset(self.insertion_off_set_from_top, value)


@bytecode('dup_x2')
class DuplicateX2(Executor):
    def execute(self):
        stack = self.machine.current_op_stack()
        peek = stack.peek_many(3)
        found = len(peek)
        if found < 2:
            raise ValueError('Stack must have at least two values to perform the dup_x2 instruction')
        first, second = peek[:2]

        first_form = found == 3 and all(CompType(item).is_one for item in peek)
        second_form = (CompType(first).is_one and CompType(second).is_two)

        if first_form:
            offset = 3
        elif second_form:
            offset = 2
        else:
            raise TypeError(f'Conditions for dup_x2 instruction were not met. Values on top-of-stack were {peek}')

        stack.insert_at_offset(offset, first.duplicate())


@bytecode('dup2')
class Duplicate2(Executor):
    def execute(self):
        stack = self.machine.current_op_stack()
        top = stack.peek()
        if CompType(top).is_two:
            stack.push(top.duplicate())
        else:
            peek = stack.peek_many(2)
            enough_values = len(peek) == 2
            right_types = all(CompType(item).is_one for item in peek)
            if not (enough_values and right_types):
                raise TypeError(f'Conditions for dup2 were not met. Values on top-of-stack were {peek}')
            for item in reversed(peek):
                stack.push(item)
