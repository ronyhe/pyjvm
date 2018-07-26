pyjvm - A jvm implementation
=====

### Why do we need another jvm implementation?
Simple answer: We don't. I made it purely for didactic purposes. 
The existing implementations are better in terms of security, compliance and performance (to name a few).

*However*, there are niche reasons one might be interested in this project

- It's much simpler than other JVMs, which is great for learning about its internals.
- It's in python, so it's fun to hack on. Most JVMs are written in low-level languages.

Some might suggest that it's a good platform for experimentation with jvm features and modifications.
This might be true, but an implementation already exists for this purpose: [Metascala](https://github.com/lihaoyi/Metascala)

### Where does this JVM diverge from the spec?
This project was written against the [JVM 8 spec](https://docs.oracle.com/javase/specs/jvms/se8/html/index.html), except:

- It does not implement the invokedynamic instruction
- It does not obey JVM arithmetic overflow rules. Instead it uses python math operations directly.
- It does little to no verification of class files
- It does little to no verification of instruction preconditions
- It rarely complies with the exceptions that instructions should throw
- It does not implement native methods

Addressing these issues should not prove very difficult. Others are welcome to tackle them.
In fact, this might prove a useful didactic task for students of various advanced topics.

### Installation
This project is compliant with usual python conventions, so to install using a virtual env:
```shell
mkdir pyjvm
cd pyjvm
git clone https://github.com/ronyhe/pyjvm.git
virtualenv venv
. venv/bin/activate
pip install .
```
Note that these steps assume that the following are installed and available on the command line:

- git
- virtualenv
- python3
- pip

Once installed you can run `pytest` to validate your installation.

### Usage
```shell
pyjvm run [OPTIONS] MAIN_CLASS
```
Where the options are:
- `-cp` (classpath) a colon separated list of class and jar files
- `--report` turns on basic tracing which will be written to stdout.

Be sure to add a standard library to your classpath. This can usually be found at *your/java/installation*/lib/rt.jar
There are other commands that are relevant to development and debugging, see pyjvm/main.py.

### High Level Architecture
The Machine in machine.py creates Frame objects that represent methods.
It loops through the frame's instructions and sends them to instructions/instructions.py, which dispatches it to
Instructor instances.
The Instructors produce instances of Action that the machine executes.

For example, let's assume that the current instruction is 'iload_0'.
This instruction should take a value, the one that resides in index 0 of the current frame's locals array.
It should push that value onto the the current frame's operand stack.

Thus, it will produce the following actions:
- Push(\<the value>)
- IncrementProgramCounter()

Which the machine will then execute. 

### Acknowledgements
There are dozens of people I learned from and dozens of tools I use every day. 
Too many to list here, so I'll point out two that were especially relevant in this project. 
I'd like to thank the creators and maintainers of:

- The [JVM specification](https://docs.oracle.com/javase/specs/jvms/se8/html/index.html) (Oracle and previously Sun)
- The [jawa python library](https://github.com/TkTech/Jawa) (TkTech)
 