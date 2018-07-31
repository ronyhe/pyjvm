### Simple example
Let's create the file Main.java. 
We expect this class to store the int value 10 in the static variable `someInt`.
```java
public class Main {
    public static int someInt = 5;

    public static void main(String[] args) {
        someInt++;
        someInt = someInt + 4;
    }
}
```

And compile it using a standard compiler.
```bash
javac Main.java
```

When we run it with tracing in pyjvm, like this:
```bash
pyjvm run Main -cp=$PWD --report
```
We see this action near the end:
```text
PutStatic(class_name='Main', field_name='someInt', value=JvmValue(<Integer>, 10))
```
So, our expectations were met. 
When using pyjvm, this class indeed stores the int value 10 in the static variable `someInt`.

Here is the full output:
```text
|  Main#<clinit>()V, Instruction(mnemonic='iconst_5', opcode=8, operands=[], pos=0)
|    Push(value=JvmValue(<Integer>, 5))
|    IncrementProgramCounter()
|  
|  Main#<clinit>()V, Instruction(mnemonic='putstatic', opcode=179, operands=[Operand(op_type=<OperandTypes.CONSTANT_INDEX: 30>, value=2)], pos=1)
|    Pop(amount=1)
|    PutStatic(class_name='Main', field_name='someInt', value=JvmValue(<Integer>, 5))
|    IncrementProgramCounter()
|  
|  Main#<clinit>()V, Instruction(mnemonic='return', opcode=177, operands=[], pos=4)
|    ReturnVoid()

|  Main#main([Ljava/lang/String;)V, Instruction(mnemonic='getstatic', opcode=178, operands=[Operand(op_type=<OperandTypes.CONSTANT_INDEX: 30>, value=2)], pos=0)
|    Push(value=JvmValue(<Integer>, 5))
|    IncrementProgramCounter()
|  
|  Main#main([Ljava/lang/String;)V, Instruction(mnemonic='iconst_1', opcode=4, operands=[], pos=3)
|    Push(value=JvmValue(<Integer>, 1))
|    IncrementProgramCounter()
|  
|  Main#main([Ljava/lang/String;)V, Instruction(mnemonic='iadd', opcode=96, operands=[], pos=4)
|    Pop(amount=2)
|    Push(value=JvmValue(<Integer>, 6))
|    IncrementProgramCounter()
|  
|  Main#main([Ljava/lang/String;)V, Instruction(mnemonic='putstatic', opcode=179, operands=[Operand(op_type=<OperandTypes.CONSTANT_INDEX: 30>, value=2)], pos=5)
|    Pop(amount=1)
|    PutStatic(class_name='Main', field_name='someInt', value=JvmValue(<Integer>, 6))
|    IncrementProgramCounter()
|  
|  Main#main([Ljava/lang/String;)V, Instruction(mnemonic='getstatic', opcode=178, operands=[Operand(op_type=<OperandTypes.CONSTANT_INDEX: 30>, value=2)], pos=8)
|    Push(value=JvmValue(<Integer>, 6))
|    IncrementProgramCounter()
|  
|  Main#main([Ljava/lang/String;)V, Instruction(mnemonic='iconst_4', opcode=7, operands=[], pos=11)
|    Push(value=JvmValue(<Integer>, 4))
|    IncrementProgramCounter()
|  
|  Main#main([Ljava/lang/String;)V, Instruction(mnemonic='iadd', opcode=96, operands=[], pos=12)
|    Pop(amount=2)
|    Push(value=JvmValue(<Integer>, 10))
|    IncrementProgramCounter()
|  
|  Main#main([Ljava/lang/String;)V, Instruction(mnemonic='putstatic', opcode=179, operands=[Operand(op_type=<OperandTypes.CONSTANT_INDEX: 30>, value=2)], pos=13)
|    Pop(amount=1)
|    PutStatic(class_name='Main', field_name='someInt', value=JvmValue(<Integer>, 10))
|    IncrementProgramCounter()
|  
|  Main#main([Ljava/lang/String;)V, Instruction(mnemonic='return', opcode=177, operands=[], pos=16)
|    ReturnVoid()
```
