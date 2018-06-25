from pyjvm.stack import Stack


def test_stack_offset():
    stack = Stack([1, 2])
    stack.insert_at_offset(3, 3)
    assert list(stack.peek_many(3)) == [1, 2, 3]


def test_stack_offset_many():
    stack = Stack([1, 2])
    stack.insert_at_offset(1, 5)
    assert list(stack.peek_many(3)) == [1, 5, 2]
    stack.insert_at_offset(1, 6)
    assert list(stack.peek_many(4)) == [1, 6, 5, 2]
