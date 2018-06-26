import operator

from pyjvm.instructions.instructions import Executor, bytecode
from pyjvm.instructions.verifiers import verifier_by_type
from pyjvm.jvm_types import min_max_by_type, Integer


@bytecode('iadd', Integer, operator.add)
class BinOp(Executor):
    def __init__(self, instruction, machine, type_, operator_):
        super().__init__(instruction, machine)
        self.type = type_
        self.operator = operator_

    def execute(self):
        stack = self.machine.current_op_stack()
        operands = [stack.pop(), stack.pop()]
        verifier = verifier_by_type(self.type)
        for op in operands:
            verifier(op)
        values = [op.value for op in operands]
        raw_result = self.operator(*values)
        min_, max_ = min_max_by_type(self.type)
        if raw_result < min_ or raw_result > max_:
            raise OverflowError('Non-JVM-compliant error. Result of math instruction out of range')
        result = self.type.create_instance(raw_result)
        stack.push(result)
