from pyjvm.instructions.instructions import Executor, bytecode
from pyjvm.instructions.verifiers import verifier_by_type
from pyjvm.jvm_types import Long, Integer, Float, Double

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


def _conversion_decorator(the_class):
    for instruction in _instructions:
        source_letter, _, target_letter = instruction
        source_type = _letters[source_letter]
        target_type = _letters[target_letter]
        func = bytecode(instruction, source_type, target_type)
        the_class = func(the_class)

    return the_class


@_conversion_decorator
class Convert(Executor):
    def __init__(self, instruction, machine, source_type, target_type):
        super().__init__(instruction, machine)
        self.source_type = source_type
        self.target_type = target_type

    def execute(self):
        stack = self.machine.current_op_stack()
        item = stack.pop()
        verifier = verifier_by_type(self.source_type)
        verifier(item)
        value = item.value
        new_item = self.target_type.create_instance(value)
        stack.push(new_item)
