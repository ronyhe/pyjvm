from pyjvm import actions
from pyjvm.instructions.instructions import Instructor, bytecode_list, bytecode

# noinspection SpellCheckingInspection
_RETURN_LETTERS = 'ilfda'
RETURN_RESULT_INSTRUCTIONS = [
    letter + 'return' for letter in _RETURN_LETTERS
]


@bytecode_list(RETURN_RESULT_INSTRUCTIONS)
class ReturnResult(Instructor):
    def execute(self):
        result = self.peek_op_stack()
        return actions.ReturnResult(result)


@bytecode('return')
class ReturnVoid(Instructor):
    def execute(self):
        return actions.ReturnVoid()
