from pyjvm import actions
from pyjvm.actions import IncrementProgramCounter
from pyjvm.instructions.instructions import Instructor, bytecode_dict, bytecode_list
from pyjvm.model.jvm_types import Integer, NULL_VALUE, Long, Float, Double
from pyjvm.utils.jawa_conversions import convert_constant


def _create_push_constants_dict():
    """Create a dictionary from instruction names to the objects they should push onto the stack

    Looks roughly like this:
    {
        iconst_0: Integer.create_instance(0),
        iconst_1: Integer.create_instance(1),
        ...
        dconst_0: Double.create_instance(0)
        dconst_1: Double.create_instance(1)
    }
    """
    dic = {
        'iconst_m1': Integer.create_instance(-1),
        'aconst_null': NULL_VALUE
    }

    specs = (
        ('i', Integer, 5),
        ('f', Float, 2),
        ('l', Long, 1),
        ('d', Double, 1),
    )
    for prefix, type_, max_value in specs:
        for value in range(max_value + 1):
            name = prefix + 'const_' + str(value)
            dic[name] = type_.create_instance(value)

    return dic


CONSTANT_VALUES = _create_push_constants_dict()
_AS_LISTS = {k: [v] for k, v in CONSTANT_VALUES.items()}  # bytecode_dict expects a list


@bytecode_dict(_AS_LISTS)
class Push(Instructor):
    """Pushes a predefined constant"""

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
        """Pushes the literal operand provided in the instruction"""
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
    """Pushes a constant from `self.constants`"""

    def execute(self):
        index = self.operand_as_int()
        constant = self.constants[index]
        return IncrementProgramCounter.after(
            actions.Push(convert_constant(constant))
        )
