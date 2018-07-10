from pyjvm import actions
from pyjvm.actions import IncrementProgramCounter
from pyjvm.instructions.instructions import bytecode_dict, Instructor
from pyjvm.jvm_types import Long, Float, Double, Integer

_letters = {
    'l': Long,
    'f': Float,
    'd': Double,
    'i': Integer,
    'b': Integer,
    'c': Integer,
    's': Integer
}


_instructions = 'i2l, i2f, i2d, l2i, l2f, l2d, f2i, f2l, f2d, d2i, d2l, d2f, i2b, i2c, i2s'.split(', ')


def _create_instruction_dict():
    dic = {}
    for name in _instructions:
        source_letter, target_letter = name.split('2')
        source, target = _letters[source_letter], _letters[target_letter]
        dic[name] = (source, target)

    return dic


CONVERSION_DICT = _create_instruction_dict()


@bytecode_dict(CONVERSION_DICT)
class Convert(Instructor):
    # noinspection PyUnusedLocal
    def __init__(self, inputs, source, target):
        super().__init__(inputs)
        self.target = target

    def execute(self):
        value = self.peek_op_stack().value
        converted = self.target.create_instance(value)
        return IncrementProgramCounter.after(
            actions.Pop(),
            actions.Push(converted)
        )
