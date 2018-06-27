from pyjvm.instructions.instructions import Executor, bytecode


@bytecode('putstatic')
class PutStatic(Executor):
    def execute(self):
        field_ref_index = int(self.instruction.operands[0].value)
        field_ref = self.machine.current_constants()[field_ref_index]
        class_name = field_ref.class_.name.value
        field_name = field_ref.name_and_type.name.value
        value = self.machine.current_op_stack().pop()
        self.machine.put_static_field(class_name, field_name, value)


@bytecode('getstatic')
class GetStatic(Executor):
    def execute(self):
        field_ref_index = int(self.instruction.operands[0].value)
        field_ref = self.machine.current_constants()[field_ref_index]
        class_name = field_ref.class_.name.value
        field_name = field_ref.name_and_type.name.value
        value = self.machine.get_static_field(class_name, field_name)
        self.machine.current_op_stack().push(value)
