# def test_int_store():
#     instruction = Instruction.create('istore', [Operand(OperandTypes.LITERAL, index)])
#     inputs = TestInputs(instruction, op_stack=Stack([Integer.create_instance(6)]))
#     actions = execute_instruction(inputs)
#     assert actions == [StoreInLocals(value=Integer.create_instance(6), index=index)]
