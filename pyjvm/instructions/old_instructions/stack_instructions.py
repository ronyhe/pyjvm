from pyjvm.instructions.instructions import Executor, bytecode
from pyjvm.jvm_types import CompType


def _comp_types(actual, *expected_numbers):
    for ex, actual in zip(expected_numbers, actual):
        num = 1 if CompType(actual).is_one else 2
        if not num == ex:
            return False

    return True


class _Form:
    def __init__(self, comp_types, offset, indexes):
        self.comp_types = [int(i) for i in comp_types]
        self.offset = offset
        try:
            self.indexes = list(indexes)
        except TypeError:
            self.indexes = [indexes]

    def matches(self, stack):
        return _comp_types(iter(stack), *self.comp_types)

    def execute(self, stack):
        values = [stack.peek(index) for index in self.indexes]
        for value in reversed(values):
            stack.insert_at_offset(self.offset, value.duplicate())


def _comp_type_forms(instruction_name, stack, *forms):
    for form in forms:
        if form.matches(stack):
            form.execute(stack)
            return

    raise TypeError(f'Conditions were no met for instruction {instruction_name}')


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
        _comp_type_forms(
            'dup_x2',
            self.machine.current_op_stack(),
            _Form(
                comp_types='111',
                offset=3,
                indexes=0
            ),
            _Form(
                comp_types='12',
                offset=2,
                indexes=0
            )
        )


@bytecode('dup2')
class Duplicate2(Executor):
    def execute(self):
        _comp_type_forms(
            'dup2',
            self.machine.current_op_stack(),
            _Form(
                comp_types='11',
                offset=0,
                indexes=(0, 1)
            ),
            _Form(
                comp_types='2',
                offset=0,
                indexes=0
            ),
        )


@bytecode('dup2_x1')
class Duplicate2X1(Executor):
    def execute(self):
        _comp_type_forms(
            'dup2_x1',
            self.machine.current_op_stack(),
            _Form(
                comp_types='111',
                offset=3,
                indexes=(0, 1)
            ),
            _Form(
                comp_types='21',
                offset=2,
                indexes=0
            )
        )


@bytecode('dup2_x2')
class Duplicate2X2(Executor):
    def execute(self):
        _comp_type_forms(
            'dup2_x2',
            self.machine.current_op_stack(),
            _Form(
                comp_types='1111',
                offset=4,
                indexes=(0, 1)
            ),
            _Form(
                comp_types='211',
                offset=4,
                indexes=0
            ),
            _Form(
                comp_types='112',
                offset=3,
                indexes=(0, 1),
            ),
            _Form(
                comp_types='22',
                offset=3,
                indexes=0
            )
        )


@bytecode('swap')
class Swap(Executor):
    def execute(self):
        stack = self.machine.current_op_stack()
        if not _comp_types(stack, 1, 1):
            raise TypeError('Top-of-stack must have two type-one-computational values for swap instruction. '
                            f'Actual values were {stack.peek_many(2)}')

        first = stack.pop()
        second = stack.pop()
        stack.push(first)
        stack.push(second)
