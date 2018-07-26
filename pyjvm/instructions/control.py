from pyjvm import actions
from pyjvm.actions import Actions
from pyjvm.instructions.instructions import Instructor, bytecode_list, bytecode, bytecode_dict
# noinspection SpellCheckingInspection
from pyjvm.instructions.switches import LOOKUP_SWITCH, TABLE_SWITCH, TableSwitch, LookupSwitch

# noinspection SpellCheckingInspection
RETURN_RESULT_INSTRUCTIONS = [
    letter + 'return' for letter in 'ilfda'
]


@bytecode_list(RETURN_RESULT_INSTRUCTIONS)
class ReturnResult(Instructor):
    """Returns from a method with the value at top-of-stack"""

    def execute(self):
        result = self.peek_op_stack()
        return actions.ReturnResult(result)


@bytecode('return')
class ReturnVoid(Instructor):
    """Returns from a method without a value"""

    def execute(self):
        return actions.ReturnVoid()


@bytecode_list([
    'goto',
    'goto_w'
])
class GoTo(Instructor):
    """Jump instructions

    The instructions provide offsets, so this Instructor adds the current program counter,
    creating an absolute value.

    There is no need to handle the goto_w instruction specially.
    The good people of the jawa library handle this during instruction parsing. Go jawa!
    """

    def execute(self):
        source = self.instruction.pos
        offset = self.operand_as_int()
        target = source + offset
        return actions.GoTo(target)


@bytecode_dict({
    TABLE_SWITCH: [TableSwitch],
    LOOKUP_SWITCH: [LookupSwitch]
})
class Switch(Instructor):
    """An instructor for complex jump instructions

    The heavy lifting occurs via the `TableSwitch` and `LookupSwitch` classes.
    See switches.py for more information.
    """

    def __init__(self, inputs, switch_class):
        super().__init__(inputs)
        self.switch_class = switch_class

    def execute(self):
        source = self.instruction.pos
        value = self.peek_op_stack()
        switch = self.switch_class.from_instruction(self.instruction)
        offset = switch.find_offset(value.value)
        target = source + offset
        return Actions(
            actions.Pop(),
            actions.GoTo(target)
        )
