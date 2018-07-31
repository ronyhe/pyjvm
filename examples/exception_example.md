### Exception Handling
Let's change Main.java from the [previous example](instance_example.md) to rely on exceptions:
```java
public class Main {
    public static int someInt;

    public static void main(String[] args) {
        try {
            Main instance = new Main(5);
            instance.add(3);
            instance.add(2);
            someInt = instance.getNum();
        }
        catch (NullPointerException ex) {
            someInt = 20;
        } 
    }

    private int num;

    public Main(int num) {
        this.num = num;
        throw new NullPointerException();
    }

    public void add(int a) {
        num += a;
    }

    public int getNum() {
        return num;
    }
}
```

We wrapped the previous functionality in a try-catch clause.
And since we added a `throw` in the constructor we expect it to be totally skipped.
Instead, we expect the value of `someInt` to be 20.
An indeed, near the end, we see:
```text
PutStatic(class_name='Main', field_name='someInt', value=JvmValue(<Integer>, 20))
```

You can see the flow in the full output:
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
|  |  Main#<init>(I)V, Instruction(mnemonic='invokespecial', opcode=183, operands=[Operand(op_type=<OperandTypes.CONSTANT_INDEX: 30>, value=7)], pos=1)
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
|  |  Main#<init>(I)V, Instruction(mnemonic='putfield', opcode=181, operands=[Operand(op_type=<OperandTypes.CONSTANT_INDEX: 30>, value=8)], pos=6)
|  |    Pop(amount=2)
|  |    PutField(object_=JvmValue(ObjectReferenceType(refers_to=Main), <JvmObject>), field_name='num', value=JvmValue(<Integer>, 5))
|  |    IncrementProgramCounter()
|  |  
|  |  Main#<init>(I)V, Instruction(mnemonic='new', opcode=187, operands=[Operand(op_type=<OperandTypes.CONSTANT_INDEX: 30>, value=6)], pos=9)
|  |    PushNewInstance(java/lang/NullPointerException)
|  |    IncrementProgramCounter()
|  |  
|  |  Main#<init>(I)V, Instruction(mnemonic='dup', opcode=89, operands=[], pos=12)
|  |    DuplicateTop(amount_to_take=1, index_for_insertion=1)
|  |    IncrementProgramCounter()
|  |  
|  |  Main#<init>(I)V, Instruction(mnemonic='invokespecial', opcode=183, operands=[Operand(op_type=<OperandTypes.CONSTANT_INDEX: 30>, value=9)], pos=13)
|  |    Pop(amount=1)
|  |    Invoke(class_name='java/lang/NullPointerException', method_key=MethodKey(name='<init>', descriptor='()V'), arguments=(JvmValue(ObjectReferenceType(refers_to=java/lang/NullPointerException), <JvmObject>),))
|  |  |  
|  |  |  java/lang/NullPointerException#<init>()V, Instruction(mnemonic='aload_0', opcode=42, operands=[], pos=0)
|  |  |    Push(value=JvmValue(ObjectReferenceType(refers_to=java/lang/NullPointerException), <JvmObject>))
|  |  |    IncrementProgramCounter()
|  |  |  
|  |  |  java/lang/NullPointerException#<init>()V, Instruction(mnemonic='invokespecial', opcode=183, operands=[Operand(op_type=<OperandTypes.CONSTANT_INDEX: 30>, value=1)], pos=1)
|  |  |    Pop(amount=1)
|  |  |    Invoke(class_name='java/lang/RuntimeException', method_key=MethodKey(name='<init>', descriptor='()V'), arguments=(JvmValue(ObjectReferenceType(refers_to=java/lang/NullPointerException), <JvmObject>),))
|  |  |  |  
|  |  |  |  java/lang/RuntimeException#<init>()V, Instruction(mnemonic='aload_0', opcode=42, operands=[], pos=0)
|  |  |  |    Push(value=JvmValue(ObjectReferenceType(refers_to=java/lang/NullPointerException), <JvmObject>))
|  |  |  |    IncrementProgramCounter()
|  |  |  |  
|  |  |  |  java/lang/RuntimeException#<init>()V, Instruction(mnemonic='invokespecial', opcode=183, operands=[Operand(op_type=<OperandTypes.CONSTANT_INDEX: 30>, value=1)], pos=1)
|  |  |  |    Pop(amount=1)
|  |  |  |    Invoke(class_name='java/lang/Exception', method_key=MethodKey(name='<init>', descriptor='()V'), arguments=(JvmValue(ObjectReferenceType(refers_to=java/lang/NullPointerException), <JvmObject>),))
|  |  |  |  |  
|  |  |  |  |  java/lang/Exception#<init>()V, Instruction(mnemonic='aload_0', opcode=42, operands=[], pos=0)
|  |  |  |  |    Push(value=JvmValue(ObjectReferenceType(refers_to=java/lang/NullPointerException), <JvmObject>))
|  |  |  |  |    IncrementProgramCounter()
|  |  |  |  |  
|  |  |  |  |  java/lang/Exception#<init>()V, Instruction(mnemonic='invokespecial', opcode=183, operands=[Operand(op_type=<OperandTypes.CONSTANT_INDEX: 30>, value=1)], pos=1)
|  |  |  |  |    Pop(amount=1)
|  |  |  |  |    Invoke(class_name='java/lang/Throwable', method_key=MethodKey(name='<init>', descriptor='()V'), arguments=(JvmValue(ObjectReferenceType(refers_to=java/lang/NullPointerException), <JvmObject>),))
|  |  |  |  |  |  
|  |  |  |  |  |  java/lang/Throwable#<init>()V, Instruction(mnemonic='aload_0', opcode=42, operands=[], pos=0)
|  |  |  |  |  |    Push(value=JvmValue(ObjectReferenceType(refers_to=java/lang/NullPointerException), <JvmObject>))
|  |  |  |  |  |    IncrementProgramCounter()
|  |  |  |  |  |  
|  |  |  |  |  |  java/lang/Throwable#<init>()V, Instruction(mnemonic='aconst_null', opcode=1, operands=[], pos=1)
|  |  |  |  |  |    Push(value=JvmValue(ObjectReferenceType(refers_to=java/lang/Object), <NULL>))
|  |  |  |  |  |    IncrementProgramCounter()
|  |  |  |  |  |  
|  |  |  |  |  |  java/lang/Throwable#<init>()V, Instruction(mnemonic='checkcast', opcode=192, operands=[Operand(op_type=<OperandTypes.CONSTANT_INDEX: 30>, value=1)], pos=2)
|  |  |  |  |  |    IncrementProgramCounter()
|  |  |  |  |  |  
|  |  |  |  |  |  java/lang/Throwable#<init>()V, Instruction(mnemonic='invokespecial', opcode=183, operands=[Operand(op_type=<OperandTypes.CONSTANT_INDEX: 30>, value=2)], pos=5)
|  |  |  |  |  |    Pop(amount=2)
|  |  |  |  |  |    Invoke(class_name='java/lang/Throwable', method_key=MethodKey(name='<init>', descriptor='(Ljava/lang/String;)V'), arguments=(JvmValue(ObjectReferenceType(refers_to=java/lang/NullPointerException), <JvmObject>), JvmValue(ObjectReferenceType(refers_to=java/lang/Object), <NULL>)))
|  |  |  |  |  |  |  
|  |  |  |  |  |  |  java/lang/Throwable#<init>(Ljava/lang/String;)V, Instruction(mnemonic='aload_0', opcode=42, operands=[], pos=0)
|  |  |  |  |  |  |    Push(value=JvmValue(ObjectReferenceType(refers_to=java/lang/NullPointerException), <JvmObject>))
|  |  |  |  |  |  |    IncrementProgramCounter()
|  |  |  |  |  |  |  
|  |  |  |  |  |  |  java/lang/Throwable#<init>(Ljava/lang/String;)V, Instruction(mnemonic='invokespecial', opcode=183, operands=[Operand(op_type=<OperandTypes.CONSTANT_INDEX: 30>, value=3)], pos=1)
|  |  |  |  |  |  |    Pop(amount=1)
|  |  |  |  |  |  |    Invoke(class_name='java/lang/Object', method_key=MethodKey(name='<init>', descriptor='()V'), arguments=(JvmValue(ObjectReferenceType(refers_to=java/lang/NullPointerException), <JvmObject>),))
|  |  |  |  |  |  |  |  
|  |  |  |  |  |  |  |  java/lang/Object#<init>()V, Instruction(mnemonic='return', opcode=177, operands=[], pos=0)
|  |  |  |  |  |  |  |    ReturnVoid()
|  |  |  |  |  |  |  
|  |  |  |  |  |  |  java/lang/Throwable#<init>(Ljava/lang/String;)V, Instruction(mnemonic='aload_0', opcode=42, operands=[], pos=4)
|  |  |  |  |  |  |    Push(value=JvmValue(ObjectReferenceType(refers_to=java/lang/NullPointerException), <JvmObject>))
|  |  |  |  |  |  |    IncrementProgramCounter()
|  |  |  |  |  |  |  
|  |  |  |  |  |  |  java/lang/Throwable#<init>(Ljava/lang/String;)V, Instruction(mnemonic='aload_0', opcode=42, operands=[], pos=5)
|  |  |  |  |  |  |    Push(value=JvmValue(ObjectReferenceType(refers_to=java/lang/NullPointerException), <JvmObject>))
|  |  |  |  |  |  |    IncrementProgramCounter()
|  |  |  |  |  |  |  
|  |  |  |  |  |  |  java/lang/Throwable#<init>(Ljava/lang/String;)V, Instruction(mnemonic='putfield', opcode=181, operands=[Operand(op_type=<OperandTypes.CONSTANT_INDEX: 30>, value=4)], pos=6)
|  |  |  |  |  |  |    Pop(amount=2)
|  |  |  |  |  |  |    PutField(object_=JvmValue(ObjectReferenceType(refers_to=java/lang/NullPointerException), <JvmObject>), field_name='cause', value=JvmValue(ObjectReferenceType(refers_to=java/lang/NullPointerException), <JvmObject>))
|  |  |  |  |  |  |    IncrementProgramCounter()
|  |  |  |  |  |  |  
|  |  |  |  |  |  |  java/lang/Throwable#<init>(Ljava/lang/String;)V, Instruction(mnemonic='aload_0', opcode=42, operands=[], pos=9)
|  |  |  |  |  |  |    Push(value=JvmValue(ObjectReferenceType(refers_to=java/lang/NullPointerException), <JvmObject>))
|  |  |  |  |  |  |    IncrementProgramCounter()
|  |  |  |  |  |  |  
|  |  |  |  |  |  |  java/lang/Throwable#<init>(Ljava/lang/String;)V, Instruction(mnemonic='invokevirtual', opcode=182, operands=[Operand(op_type=<OperandTypes.CONSTANT_INDEX: 30>, value=5)], pos=10)
|  |  |  |  |  |  |    Pop(amount=1)
|  |  |  |  |  |  |    Invoke(class_name='java/lang/Throwable', method_key=MethodKey(name='fillInStackTrace', descriptor='()Ljava/lang/Throwable;'), arguments=(JvmValue(ObjectReferenceType(refers_to=java/lang/NullPointerException), <JvmObject>),))
|  |  |  |  |  |  |  |  
|  |  |  |  |  |  |  |  java/lang/Throwable#fillInStackTrace()Ljava/lang/Throwable;, Instruction(mnemonic='aload_0', opcode=42, operands=[], pos=0)
|  |  |  |  |  |  |  |    Push(value=JvmValue(ObjectReferenceType(refers_to=java/lang/NullPointerException), <JvmObject>))
|  |  |  |  |  |  |  |    IncrementProgramCounter()
|  |  |  |  |  |  |  |  
|  |  |  |  |  |  |  |  java/lang/Throwable#fillInStackTrace()Ljava/lang/Throwable;, Instruction(mnemonic='aload_0', opcode=42, operands=[], pos=1)
|  |  |  |  |  |  |  |    Push(value=JvmValue(ObjectReferenceType(refers_to=java/lang/NullPointerException), <JvmObject>))
|  |  |  |  |  |  |  |    IncrementProgramCounter()
|  |  |  |  |  |  |  |  
|  |  |  |  |  |  |  |  java/lang/Throwable#fillInStackTrace()Ljava/lang/Throwable;, Instruction(mnemonic='invokestatic', opcode=184, operands=[Operand(op_type=<OperandTypes.CONSTANT_INDEX: 30>, value=45)], pos=2)
|  |  |  |  |  |  |  |    Pop(amount=1)
|  |  |  |  |  |  |  |    Invoke(class_name='java/lang/VMThrowable', method_key=MethodKey(name='fillInStackTrace', descriptor='(Ljava/lang/Throwable;)Ljava/lang/VMThrowable;'), arguments=(JvmValue(ObjectReferenceType(refers_to=java/lang/NullPointerException), <JvmObject>),))
|  |  |  |  |  |  |  |  |  
|  |  |  |  |  |  |  |  |  java/lang/VMThrowable#fillInStackTrace(Ljava/lang/Throwable;)Ljava/lang/VMThrowable;, Instruction(mnemonic='aload_0', opcode=42, operands=[], pos=1)
|  |  |  |  |  |  |  |  |    Push(value=JvmValue(ObjectReferenceType(refers_to=java/lang/NullPointerException), <JvmObject>))
|  |  |  |  |  |  |  |  |    IncrementProgramCounter()
|  |  |  |  |  |  |  |  |  
|  |  |  |  |  |  |  |  |  java/lang/VMThrowable#fillInStackTrace(Ljava/lang/Throwable;)Ljava/lang/VMThrowable;, Instruction(mnemonic='areturn', opcode=176, operands=[], pos=2)
|  |  |  |  |  |  |  |  |    ReturnResult(result=JvmValue(ObjectReferenceType(refers_to=java/lang/NullPointerException), <JvmObject>))
|  |  |  |  |  |  |  |  
|  |  |  |  |  |  |  |  java/lang/Throwable#fillInStackTrace()Ljava/lang/Throwable;, Instruction(mnemonic='putfield', opcode=181, operands=[Operand(op_type=<OperandTypes.CONSTANT_INDEX: 30>, value=46)], pos=5)
|  |  |  |  |  |  |  |    Pop(amount=2)
|  |  |  |  |  |  |  |    PutField(object_=JvmValue(ObjectReferenceType(refers_to=java/lang/NullPointerException), <JvmObject>), field_name='vmState', value=JvmValue(ObjectReferenceType(refers_to=java/lang/NullPointerException), <JvmObject>))
|  |  |  |  |  |  |  |    IncrementProgramCounter()
|  |  |  |  |  |  |  |  
|  |  |  |  |  |  |  |  java/lang/Throwable#fillInStackTrace()Ljava/lang/Throwable;, Instruction(mnemonic='aload_0', opcode=42, operands=[], pos=8)
|  |  |  |  |  |  |  |    Push(value=JvmValue(ObjectReferenceType(refers_to=java/lang/NullPointerException), <JvmObject>))
|  |  |  |  |  |  |  |    IncrementProgramCounter()
|  |  |  |  |  |  |  |  
|  |  |  |  |  |  |  |  java/lang/Throwable#fillInStackTrace()Ljava/lang/Throwable;, Instruction(mnemonic='aconst_null', opcode=1, operands=[], pos=9)
|  |  |  |  |  |  |  |    Push(value=JvmValue(ObjectReferenceType(refers_to=java/lang/Object), <NULL>))
|  |  |  |  |  |  |  |    IncrementProgramCounter()
|  |  |  |  |  |  |  |  
|  |  |  |  |  |  |  |  java/lang/Throwable#fillInStackTrace()Ljava/lang/Throwable;, Instruction(mnemonic='putfield', opcode=181, operands=[Operand(op_type=<OperandTypes.CONSTANT_INDEX: 30>, value=47)], pos=10)
|  |  |  |  |  |  |  |    Pop(amount=2)
|  |  |  |  |  |  |  |    PutField(object_=JvmValue(ObjectReferenceType(refers_to=java/lang/NullPointerException), <JvmObject>), field_name='stackTrace', value=JvmValue(ObjectReferenceType(refers_to=java/lang/Object), <NULL>))
|  |  |  |  |  |  |  |    IncrementProgramCounter()
|  |  |  |  |  |  |  |  
|  |  |  |  |  |  |  |  java/lang/Throwable#fillInStackTrace()Ljava/lang/Throwable;, Instruction(mnemonic='aload_0', opcode=42, operands=[], pos=13)
|  |  |  |  |  |  |  |    Push(value=JvmValue(ObjectReferenceType(refers_to=java/lang/NullPointerException), <JvmObject>))
|  |  |  |  |  |  |  |    IncrementProgramCounter()
|  |  |  |  |  |  |  |  
|  |  |  |  |  |  |  |  java/lang/Throwable#fillInStackTrace()Ljava/lang/Throwable;, Instruction(mnemonic='areturn', opcode=176, operands=[], pos=14)
|  |  |  |  |  |  |  |    ReturnResult(result=JvmValue(ObjectReferenceType(refers_to=java/lang/NullPointerException), <JvmObject>))
|  |  |  |  |  |  |  
|  |  |  |  |  |  |  java/lang/Throwable#<init>(Ljava/lang/String;)V, Instruction(mnemonic='pop', opcode=87, operands=[], pos=13)
|  |  |  |  |  |  |    Pop(amount=1)
|  |  |  |  |  |  |    IncrementProgramCounter()
|  |  |  |  |  |  |  
|  |  |  |  |  |  |  java/lang/Throwable#<init>(Ljava/lang/String;)V, Instruction(mnemonic='aload_0', opcode=42, operands=[], pos=14)
|  |  |  |  |  |  |    Push(value=JvmValue(ObjectReferenceType(refers_to=java/lang/NullPointerException), <JvmObject>))
|  |  |  |  |  |  |    IncrementProgramCounter()
|  |  |  |  |  |  |  
|  |  |  |  |  |  |  java/lang/Throwable#<init>(Ljava/lang/String;)V, Instruction(mnemonic='aload_1', opcode=43, operands=[], pos=15)
|  |  |  |  |  |  |    Push(value=JvmValue(ObjectReferenceType(refers_to=java/lang/Object), <NULL>))
|  |  |  |  |  |  |    IncrementProgramCounter()
|  |  |  |  |  |  |  
|  |  |  |  |  |  |  java/lang/Throwable#<init>(Ljava/lang/String;)V, Instruction(mnemonic='putfield', opcode=181, operands=[Operand(op_type=<OperandTypes.CONSTANT_INDEX: 30>, value=6)], pos=16)
|  |  |  |  |  |  |    Pop(amount=2)
|  |  |  |  |  |  |    PutField(object_=JvmValue(ObjectReferenceType(refers_to=java/lang/NullPointerException), <JvmObject>), field_name='detailMessage', value=JvmValue(ObjectReferenceType(refers_to=java/lang/Object), <NULL>))
|  |  |  |  |  |  |    IncrementProgramCounter()
|  |  |  |  |  |  |  
|  |  |  |  |  |  |  java/lang/Throwable#<init>(Ljava/lang/String;)V, Instruction(mnemonic='return', opcode=177, operands=[], pos=19)
|  |  |  |  |  |  |    ReturnVoid()
|  |  |  |  |  |  
|  |  |  |  |  |  java/lang/Throwable#<init>()V, Instruction(mnemonic='return', opcode=177, operands=[], pos=8)
|  |  |  |  |  |    ReturnVoid()
|  |  |  |  |  
|  |  |  |  |  java/lang/Exception#<init>()V, Instruction(mnemonic='return', opcode=177, operands=[], pos=4)
|  |  |  |  |    ReturnVoid()
|  |  |  |  
|  |  |  |  java/lang/RuntimeException#<init>()V, Instruction(mnemonic='return', opcode=177, operands=[], pos=4)
|  |  |  |    ReturnVoid()
|  |  |  
|  |  |  java/lang/NullPointerException#<init>()V, Instruction(mnemonic='return', opcode=177, operands=[], pos=4)
|  |  |    ReturnVoid()
|  |  
|  |  Main#<init>(I)V, Instruction(mnemonic='athrow', opcode=191, operands=[], pos=16)
|  |    ThrowObject(value=JvmValue(ObjectReferenceType(refers_to=java/lang/NullPointerException), <JvmObject>))
|  
|  Main#main([Ljava/lang/String;)V, Instruction(mnemonic='astore_1', opcode=76, operands=[], pos=29)
|    StoreInLocals(index=1, value=JvmValue(ObjectReferenceType(refers_to=java/lang/NullPointerException), <JvmObject>))
|    Pop(amount=1)
|    IncrementProgramCounter()
|  
|  Main#main([Ljava/lang/String;)V, Instruction(mnemonic='bipush', opcode=16, operands=[Operand(op_type=<OperandTypes.LITERAL: 10>, value=20)], pos=30)
|    Push(value=JvmValue(<Integer>, 20))
|    IncrementProgramCounter()
|  
|  Main#main([Ljava/lang/String;)V, Instruction(mnemonic='putstatic', opcode=179, operands=[Operand(op_type=<OperandTypes.CONSTANT_INDEX: 30>, value=5)], pos=32)
|    Pop(amount=1)
|    PutStatic(class_name='Main', field_name='someInt', value=JvmValue(<Integer>, 20))
|    IncrementProgramCounter()
|  
|  Main#main([Ljava/lang/String;)V, Instruction(mnemonic='return', opcode=177, operands=[], pos=35)
|    ReturnVoid()
```

