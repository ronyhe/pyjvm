from pyjvm.instructions.instructions import Executor, bytecode
from pyjvm.jvm_types import CompType


def _comp_types(actual, *expected_numbers):
    for ex, actual in zip(expected_numbers, actual):
        num = 1 if CompType(actual).is_one else 2
        if not num == ex:
            return False

    return True


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
        first, second = peek[:2]

        first_form = _comp_types(peek, 1, 1, 1)
        second_form = _comp_types(peek, 1, 2)

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
        peek = stack.peek_many(2)
        top = stack.peek()

        first_form = _comp_types(peek, 2)
        second_form = _comp_types(peek, 1, 1)

        if first_form:
            stack.push(top.duplicate())
        elif second_form:
            for item in reversed(peek):
                stack.push(item.duplicate())
        else:
            raise TypeError(f'Conditions for dup2 were not met. Values on top-of-stack were {peek}')


@bytecode('dup2_x1')
class Duplicate2X1(Executor):
    def execute(self):
        stack = self.machine.current_op_stack()
        peek = stack.peek_many(3)

        first_form = _comp_types(peek, 1, 1, 1)
        second_form = _comp_types(peek, 2, 1)

        first, second, _ = peek
        if first_form:
            stack.insert_at_offset(4, first.duplicate())
            stack.insert_at_offset(4, second.duplicate())
        elif second_form:
            stack.insert_at_offset(2, first.duplicate())
        else:
            raise TypeError(f'Conditions for dup2_x1 were not met. Values on top-of-stack were {peek}')


@bytecode('dup2_x2')
class Duplicate2X2(Executor):
    def execute(self):
        stack = self.machine.current_op_stack()
        peek = stack.peek_many(4)

        first_case = _comp_types(peek, 1, 1, 1, 1)
        second_case = _comp_types(peek, 2, 1, 1)
        third_case = _comp_types(peek, 1, 1, 2)
        fourth_case = _comp_types(peek, 2, 2)

        if first_case:
            items = 0, 1
            offset = 5
        elif second_case:
            items = (0,)
            offset = 4
        elif third_case:
            items = 0, 1
            offset = 4
        elif fourth_case:
            items = (0,)
            offset = 3
        else:
            raise TypeError(f'Conditions for dup2_x2 were not met. Values on top-of-stack were {peek}')

        for index in items:
            stack.insert_at_offset(offset, peek[index].duplicate())
