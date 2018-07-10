#
# def test_class_init():
#     class_name = 'class_name'
#     the_class = ClassFile.create(class_name)
#     field_name = 'field_name'
#     field = the_class.fields.create(field_name, 'I')
#     field.access_flags.set('acc_static', True)
#     field_ref_constant = the_class.constants.create_field_ref(class_name, field_name, 'I')
#     init = the_class.methods.create(NAME_OF_STATIC_CONSTRUCTOR, '()V', code=True)
#     init.access_flags.set('acc_static', True)
#     init.code.max_locals = 10
#     init.code.max_stack = 10
#     init.code.assemble([
#         Instruction.create('iconst_5'),
#         Instruction.create('putstatic', [Operand(OperandTypes.CONSTANT_INDEX, field_ref_constant.index)]),
#     ])
#     machine = BlankTestMachine(FixedClassLoader({class_name: convert_class_file(the_class)}))
#     actual = machine.get_static_field(class_name, field_name)
#     assert actual == Integer.create_instance(5)
