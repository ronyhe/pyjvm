from pyjvm import actions
from pyjvm.actions import IncrementProgramCounter
from pyjvm.instructions.instructions import Instructor, bytecode_dict, bytecode_list
from pyjvm.jawa_conversions import convert_constant
from pyjvm.jvm_types import Integer, NULL_VALUE, Long, Float, Double


def _create_push_constants_dict():
    dic = {
        'iconst_m1': Integer.create_instance(-1),
        'aconst_null': NULL_VALUE
    }

    specs = (
        ('i', Integer, 5),
        ('l', Long, 1),
        ('f', Float, 1),
        ('d', Double, 1),
    )
    for prefix, type_, max_value in specs:
        for value in range(max_value + 1):
            name = prefix + 'const_' + str(value)
            dic[name] = type_.create_instance(value)

    return dic


CONSTANT_VALUES = _create_push_constants_dict()
_AS_LISTS = {k: [v] for k, v in CONSTANT_VALUES.items()}


@bytecode_dict(_AS_LISTS)
class Push(Instructor):
    def __init__(self, inputs, value):
        super().__init__(inputs)
        self.value = value

    def execute(self):
        return IncrementProgramCounter.after(
            actions.Push(self.value)
        )


@bytecode_list(['sipush', 'bipush'])
class PushOperand(Instructor):
    def execute(self):
        value = Integer.create_instance(self.operand_as_int())
        return IncrementProgramCounter.after(
            actions.Push(value)
        )


@bytecode_list([
    'ldc',
    'ldc_w',
    'ldc2_w'
])
class LoadFromConstantPool(Instructor):
    def execute(self):
        index = self.operand_as_int()
        constant = self.constants[index]
        return IncrementProgramCounter.after(
            actions.Push(convert_constant(constant))
        )
