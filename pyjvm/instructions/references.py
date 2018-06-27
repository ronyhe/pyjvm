from pyjvm.instructions.instructions import Executor, bytecode


# noinspection PyAbstractClass
class _ReferenceExecutor(Executor):
    def constant_from_index(self):
        index = int(self.instruction.operands[0].value)
        return self.machine.current_constants()[index]


@bytecode('putstatic')
class PutStatic(_ReferenceExecutor):
    def execute(self):
        field_ref = self.constant_from_index()
        class_name = field_ref.class_.name.value
        field_name = field_ref.name_and_type.name.value
        value = self.machine.current_op_stack().pop()
        self.machine.put_static_field(class_name, field_name, value)


@bytecode('getstatic')
class GetStatic(_ReferenceExecutor):
    def execute(self):
        field_ref = self.constant_from_index()
        class_name = field_ref.class_.name.value
        field_name = field_ref.name_and_type.name.value
        value = self.machine.get_static_field(class_name, field_name)
        self.machine.current_op_stack().push(value)


@bytecode('new')
class New(_ReferenceExecutor):
    def execute(self):
        class_ref = self.constant_from_index()
        class_name = class_ref.name.value
        value = self.machine.create_new_class_instance(class_name)
        self.machine.current_op_stack().push(value)
