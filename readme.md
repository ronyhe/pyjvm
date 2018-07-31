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


### Installation
This project is compliant with usual python conventions.
So assuming python 3.6+ and virtualenv are installed:
```bash
git clone https://github.com/ronyhe/pyjvm.git
cd pyjvm
virtualenv venv
. venv/bin/activate
python -m pip install .
```

Once installed you can run the tests to validate your installation:
```bash
pytest
```

### Usage
```bash
pyjvm run [OPTIONS] MAIN_CLASS
```
Where the options are:
- `-cp` (classpath) a colon separated list of class and jar/zip files. Similar to the Java CLASSPATH variable.
- `--report` turns on basic tracing which will be written to stdout.

There are other commands that are relevant to development and debugging, see [pyjvm/main.py](pyjvm/main.py).

### High Level Architecture
The [Machine](pyjvm/core/machine.py) creates [Frame](pyjvm/core/frame.py) objects that represent methods.
It loops through the frame's instructions and sends them to [instructions.py](pyjvm/instructions/instructions.py), 
which dispatches them to [Instructor](pyjvm/instructions/instructions.py) instances.
The Instructors produce instances of [Action](pyjvm/core/actions.py) that the machine executes.

For example, let's assume that the current instruction is 'iload_0'.
This instruction should take a value, the one that resides in index 0 of the current frame's locals array.
It should push that value onto the the current frame's operand stack.

Thus, it will produce the following actions:
- Push(\<the value>)
- IncrementProgramCounter()

Which the machine will then execute. 


### Where does this JVM diverge from the spec?
This project was written against the [JVM 8 spec](https://docs.oracle.com/javase/specs/jvms/se8/html/index.html), except:

- It does not implement the invokedynamic instruction
- It does not obey JVM arithmetic overflow rules. Instead it uses python math operations directly.
- It does little to no verification of class files
- It does little to no verification of instruction preconditions
- It rarely complies with the exceptions that instructions should throw*.
- It does not implement native methods
- It does not implement the jsr and ret instructions**


Others are welcome to tackle these issues if they wish.
In fact, this might prove a useful didactic task for students of various advanced topics.

*Most (but not all) of the exceptions that instructions should throw are related to faulty class files.
 These cases are security features that aren't relevant to a non-production VM. 

**Note that the jsr and ret instructions are, to my understanding, largely obsolete.
Modern Java compilers do not emit them (although other JVM languages might) and the specification discourages their use.
See [this stackoverflow discussion](https://stackoverflow.com/a/21150629). 


### Java Standard Library
Since there is no native method support, most standard library functionality will not be available.
The project has a standard library mainly for useful class definitions. 
Especially the builtin Java exceptions, some of which are included in the JVM specification itself.

The included implementation is the one provided 
by the [GNU classpath project](https://www.gnu.org/software/classpath/).
It's designed with alternative JVMs in mind, so adding full support could be a natural evolution for the pyjvm project. 

Another possible evolution is to convert the project to Jython.
In that case we can use the reflection API of the underlying JVM to call standard library methods.
In a way, that would make the project [meta-circular](https://en.wikipedia.org/wiki/Meta-circular_evaluator).


### Acknowledgements
There are dozens of people I learned from and dozens of tools I use every day. 
Too many to list here, so I'll point out two that were especially relevant in this project. 
I'd like to thank the creators and maintainers of:

- The [GNU classpath project](https://www.gnu.org/software/classpath/)
- The [JVM specification](https://docs.oracle.com/javase/specs/jvms/se8/html/index.html) (Oracle and previously Sun)
- The [jawa python library](https://github.com/TkTech/Jawa) (TkTech)
 