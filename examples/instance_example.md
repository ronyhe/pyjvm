### Something a bit more complex
Let's change Main.java from the [previous example](simple_example.md) and recompile:
```java
public class Main {
    public static int someInt;

    public static void main(String[] args) {
        Main instance = new Main(5);
        instance.add(3);
        instance.add(2);
        someInt = instance.getNum();
    }

    private int num;

    public Main(int num) {
        this.num = num;
    }

    public void add(int a) {
        num += a;
    }

    public int getNum() {
        return num;
    }
}
```
We still expect it to store 10 in `someInt`, but there's more going on here:
- Instance creation
- Instance state
- Method calls, with and without return values.
- Method calls, with and without parameters.

When we run it using the same command, we still see this action near the end:
```text
PutStatic(class_name='Main', field_name='someInt', value=JvmValue(<Integer>, 10))
```

You can see the general flow of method calls in the full output:
```text
|  Main#main([Ljava/lang/String;)V, Instruction(mnemonic='new', opcode=187, operands=[Operand(op_type=<OperandTypes.CONSTANT_INDEX: 30>, value=1)], pos=0)
|    PushNewInstance(Main)
|    IncrementProgramCounter()
|  
|  Main#main([Ljava/lang/String;)V, Instruction(mnemonic='dup', opcode=89, operands=[], pos=3)
|    DuplicateTop(amount_to_take=1, index_for_insertion=1)
|    IncrementProgramCounter()
|  
|  Main#main([Ljava/lang/String;)V, Instruction(mnemonic='iconst_5', opcode=8, operands=[], pos=4)
|    Push(value=JvmValue(<Integer>, 5))
|    IncrementProgramCounter()
|  
|  Main#main([Ljava/lang/String;)V, Instruction(mnemonic='invokespecial', opcode=183, operands=[Operand(op_type=<OperandTypes.CONSTANT_INDEX: 30>, value=2)], pos=5)
|    Pop(amount=2)
|    Invoke(class_name='Main', method_key=MethodKey(name='<init>', descriptor='(I)V'), arguments=(JvmValue(ObjectReferenceType(refers_to=Main), <JvmObject>), JvmValue(<Integer>, 5)))
|  |  
|  |  Main#<init>(I)V, Instruction(mnemonic='aload_0', opcode=42, operands=[], pos=0)
|  |    Push(value=JvmValue(ObjectReferenceType(refers_to=Main), <JvmObject>))
|  |    IncrementProgramCounter()
|  |  
|  |  Main#<init>(I)V, Instruction(mnemonic='invokespecial', opcode=183, operands=[Operand(op_type=<OperandTypes.CONSTANT_INDEX: 30>, value=6)], pos=1)
|  |    Pop(amount=1)
|  |    Invoke(class_name='java/lang/Object', method_key=MethodKey(name='<init>', descriptor='()V'), arguments=(JvmValue(ObjectReferenceType(refers_to=Main), <JvmObject>),))
|  |  |  
|  |  |  java/lang/Object#<init>()V, Instruction(mnemonic='return', opcode=177, operands=[], pos=0)
|  |  |    ReturnVoid()
|  |  
|  |  Main#<init>(I)V, Instruction(mnemonic='aload_0', opcode=42, operands=[], pos=4)
|  |    Push(value=JvmValue(ObjectReferenceType(refers_to=Main), <JvmObject>))
|  |    IncrementProgramCounter()
|  |  
|  |  Main#<init>(I)V, Instruction(mnemonic='iload_1', opcode=27, operands=[], pos=5)
|  |    Push(value=JvmValue(<Integer>, 5))
|  |    IncrementProgramCounter()
|  |  
|  |  Main#<init>(I)V, Instruction(mnemonic='putfield', opcode=181, operands=[Operand(op_type=<OperandTypes.CONSTANT_INDEX: 30>, value=7)], pos=6)
|  |    Pop(amount=2)
|  |    PutField(object_=JvmValue(ObjectReferenceType(refers_to=Main), <JvmObject>), field_name='num', value=JvmValue(<Integer>, 5))
|  |    IncrementProgramCounter()
|  |  
|  |  Main#<init>(I)V, Instruction(mnemonic='return', opcode=177, operands=[], pos=9)
|  |    ReturnVoid()
|  
|  Main#main([Ljava/lang/String;)V, Instruction(mnemonic='astore_1', opcode=76, operands=[], pos=8)
|    StoreInLocals(index=1, value=JvmValue(ObjectReferenceType(refers_to=Main), <JvmObject>))
|    Pop(amount=1)
|    IncrementProgramCounter()
|  
|  Main#main([Ljava/lang/String;)V, Instruction(mnemonic='aload_1', opcode=43, operands=[], pos=9)
|    Push(value=JvmValue(ObjectReferenceType(refers_to=Main), <JvmObject>))
|    IncrementProgramCounter()
|  
|  Main#main([Ljava/lang/String;)V, Instruction(mnemonic='iconst_3', opcode=6, operands=[], pos=10)
|    Push(value=JvmValue(<Integer>, 3))
|    IncrementProgramCounter()
|  
|  Main#main([Ljava/lang/String;)V, Instruction(mnemonic='invokevirtual', opcode=182, operands=[Operand(op_type=<OperandTypes.CONSTANT_INDEX: 30>, value=3)], pos=11)
|    Pop(amount=2)
|    Invoke(class_name='Main', method_key=MethodKey(name='add', descriptor='(I)V'), arguments=(JvmValue(ObjectReferenceType(refers_to=Main), <JvmObject>), JvmValue(<Integer>, 3)))
|  |  
|  |  Main#add(I)V, Instruction(mnemonic='aload_0', opcode=42, operands=[], pos=0)
|  |    Push(value=JvmValue(ObjectReferenceType(refers_to=Main), <JvmObject>))
|  |    IncrementProgramCounter()
|  |  
|  |  Main#add(I)V, Instruction(mnemonic='dup', opcode=89, operands=[], pos=1)
|  |    DuplicateTop(amount_to_take=1, index_for_insertion=1)
|  |    IncrementProgramCounter()
|  |  
|  |  Main#add(I)V, Instruction(mnemonic='getfield', opcode=180, operands=[Operand(op_type=<OperandTypes.CONSTANT_INDEX: 30>, value=7)], pos=2)
|  |    Pop(amount=1)
|  |    Push(value=JvmValue(<Integer>, 5))
|  |    IncrementProgramCounter()
|  |  
|  |  Main#add(I)V, Instruction(mnemonic='iload_1', opcode=27, operands=[], pos=5)
|  |    Push(value=JvmValue(<Integer>, 3))
|  |    IncrementProgramCounter()
|  |  
|  |  Main#add(I)V, Instruction(mnemonic='iadd', opcode=96, operands=[], pos=6)
|  |    Pop(amount=2)
|  |    Push(value=JvmValue(<Integer>, 8))
|  |    IncrementProgramCounter()
|  |  
|  |  Main#add(I)V, Instruction(mnemonic='putfield', opcode=181, operands=[Operand(op_type=<OperandTypes.CONSTANT_INDEX: 30>, value=7)], pos=7)
|  |    Pop(amount=2)
|  |    PutField(object_=JvmValue(ObjectReferenceType(refers_to=Main), <JvmObject>), field_name='num', value=JvmValue(<Integer>, 8))
|  |    IncrementProgramCounter()
|  |  
|  |  Main#add(I)V, Instruction(mnemonic='return', opcode=177, operands=[], pos=10)
|  |    ReturnVoid()
|  
|  Main#main([Ljava/lang/String;)V, Instruction(mnemonic='aload_1', opcode=43, operands=[], pos=14)
|    Push(value=JvmValue(ObjectReferenceType(refers_to=Main), <JvmObject>))
|    IncrementProgramCounter()
|  
|  Main#main([Ljava/lang/String;)V, Instruction(mnemonic='iconst_2', opcode=5, operands=[], pos=15)
|    Push(value=JvmValue(<Integer>, 2))
|    IncrementProgramCounter()
|  
|  Main#main([Ljava/lang/String;)V, Instruction(mnemonic='invokevirtual', opcode=182, operands=[Operand(op_type=<OperandTypes.CONSTANT_INDEX: 30>, value=3)], pos=16)
|    Pop(amount=2)
|    Invoke(class_name='Main', method_key=MethodKey(name='add', descriptor='(I)V'), arguments=(JvmValue(ObjectReferenceType(refers_to=Main), <JvmObject>), JvmValue(<Integer>, 2)))
|  |  
|  |  Main#add(I)V, Instruction(mnemonic='aload_0', opcode=42, operands=[], pos=0)
|  |    Push(value=JvmValue(ObjectReferenceType(refers_to=Main), <JvmObject>))
|  |    IncrementProgramCounter()
|  |  
|  |  Main#add(I)V, Instruction(mnemonic='dup', opcode=89, operands=[], pos=1)
|  |    DuplicateTop(amount_to_take=1, index_for_insertion=1)
|  |    IncrementProgramCounter()
|  |  
|  |  Main#add(I)V, Instruction(mnemonic='getfield', opcode=180, operands=[Operand(op_type=<OperandTypes.CONSTANT_INDEX: 30>, value=7)], pos=2)
|  |    Pop(amount=1)
|  |    Push(value=JvmValue(<Integer>, 8))
|  |    IncrementProgramCounter()
|  |  
|  |  Main#add(I)V, Instruction(mnemonic='iload_1', opcode=27, operands=[], pos=5)
|  |    Push(value=JvmValue(<Integer>, 2))
|  |    IncrementProgramCounter()
|  |  
|  |  Main#add(I)V, Instruction(mnemonic='iadd', opcode=96, operands=[], pos=6)
|  |    Pop(amount=2)
|  |    Push(value=JvmValue(<Integer>, 10))
|  |    IncrementProgramCounter()
|  |  
|  |  Main#add(I)V, Instruction(mnemonic='putfield', opcode=181, operands=[Operand(op_type=<OperandTypes.CONSTANT_INDEX: 30>, value=7)], pos=7)
|  |    Pop(amount=2)
|  |    PutField(object_=JvmValue(ObjectReferenceType(refers_to=Main), <JvmObject>), field_name='num', value=JvmValue(<Integer>, 10))
|  |    IncrementProgramCounter()
|  |  
|  |  Main#add(I)V, Instruction(mnemonic='return', opcode=177, operands=[], pos=10)
|  |    ReturnVoid()
|  
|  Main#main([Ljava/lang/String;)V, Instruction(mnemonic='aload_1', opcode=43, operands=[], pos=19)
|    Push(value=JvmValue(ObjectReferenceType(refers_to=Main), <JvmObject>))
|    IncrementProgramCounter()
|  
|  Main#main([Ljava/lang/String;)V, Instruction(mnemonic='invokevirtual', opcode=182, operands=[Operand(op_type=<OperandTypes.CONSTANT_INDEX: 30>, value=4)], pos=20)
|    Pop(amount=1)
|    Invoke(class_name='Main', method_key=MethodKey(name='getNum', descriptor='()I'), arguments=(JvmValue(ObjectReferenceType(refers_to=Main), <JvmObject>),))
|  |  
|  |  Main#getNum()I, Instruction(mnemonic='aload_0', opcode=42, operands=[], pos=0)
|  |    Push(value=JvmValue(ObjectReferenceType(refers_to=Main), <JvmObject>))
|  |    IncrementProgramCounter()
|  |  
|  |  Main#getNum()I, Instruction(mnemonic='getfield', opcode=180, operands=[Operand(op_type=<OperandTypes.CONSTANT_INDEX: 30>, value=7)], pos=1)
|  |    Pop(amount=1)
|  |    Push(value=JvmValue(<Integer>, 10))
|  |    IncrementProgramCounter()
|  |  
|  |  Main#getNum()I, Instruction(mnemonic='ireturn', opcode=172, operands=[], pos=4)
|  |    ReturnResult(result=JvmValue(<Integer>, 10))
|  
|  Main#main([Ljava/lang/String;)V, Instruction(mnemonic='putstatic', opcode=179, operands=[Operand(op_type=<OperandTypes.CONSTANT_INDEX: 30>, value=5)], pos=23)
|    Pop(amount=1)
|    PutStatic(class_name='Main', field_name='someInt', value=JvmValue(<Integer>, 10))
|    IncrementProgramCounter()
|  
|  Main#main([Ljava/lang/String;)V, Instruction(mnemonic='return', opcode=177, operands=[], pos=26)
|    ReturnVoid()
```
