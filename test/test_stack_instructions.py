from pyjvm.actions import Pop, DuplicateTop
from pyjvm.jvm_types import Integer, Long
from test.utils import assert_incrementing_instruction, SOME_INT


def _create_integers(amount):
    for i in range(amount):
        yield Integer.create_instance(i)


def _translate_stack_string(text):
    def elem(e):
        if e == '1':
            type_ = Integer
        elif e == '2':
            type_ = Long
        else:
            raise ValueError()

        return type_.create_instance(4)

    return [elem(c) for c in text]


def _duplication_test(instruction, stack_string, amount_to_take, index_for_insertion):
    assert_incrementing_instruction(
        instruction=instruction,
        op_stack=_translate_stack_string(stack_string),
        expected=[
            DuplicateTop(amount_to_take=amount_to_take, index_for_insertion=index_for_insertion)
        ]
    )


def _duplication_tests(specs):
    for spec in specs:
        _duplication_test(*spec)


def test_duplications():
    _duplication_tests((
        ('dup', '1', 1, 1),
        ('dup_x1', '11', 1, 2),
        ('dup_x2', '111', 1, 3),
        ('dup_x2', '12', 1, 2),
        ('dup2', '11', 2, 2),
        ('dup2', '2', 1, 1),
        ('dup2_x1', '111', 2, 3),
        ('dup2_x1', '21', 1, 2),
        ('dup2_x2', '1111', 2, 4),
        ('dup2_x2', '211', 1, 3),
        ('dup2_x2', '112', 2, 3),
        ('dup2_x2', '22', 1, 2)
    ))


def test_pop():
    assert_incrementing_instruction(
        instruction='pop',
        op_stack=[SOME_INT],
        expected=[Pop()]
    )
