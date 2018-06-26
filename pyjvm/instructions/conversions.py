from pyjvm.instructions.instructions import Executor, bytecode
from pyjvm.instructions.verifiers import verifier_by_type
from pyjvm.jvm_types import Long, Integer, Float


@bytecode('i2l', Integer, Long)
@bytecode('i2f', Integer, Float)
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
