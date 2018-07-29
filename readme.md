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
- It does not implement the jsr and ret instructions

Note that the jsr and ret instructions are, to my understanding, largely obsolete.
Modern Java compiler do not emit them (although other JVM languages might) and the specification discourages their use.
See [this stackoverflow discutssion](https://stackoverflow.com/a/21150629). 

Addressing these issues should not prove very difficult. Others are welcome to tackle them.
In fact, this might prove a useful didactic task for students of various advanced topics.

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
pytest std_lib=path/to/std/lib/jar_file.jar
```
See the standard library section of this document to understand the `std_lib` command line variable.

### Usage
```bash
pyjvm run [OPTIONS] MAIN_CLASS
```
Where the options are:
- `-cp` (classpath) a colon separated list of class and jar/zip files. Similar to the Java CLASSPATH variable.
- `--report` turns on basic tracing which will be written to stdout.

Be sure to add a standard library to your classpath. See the standard library section of this document for more. 

There are other commands that are relevant to development and debugging, see pyjvm/main.py.

### Java Standard Library
All non trivial Java class files will need access to a standard library.
In fact, many trivial ones will need it as well.
Perhaps surprisingly, even when running class files that were compiled from other JVM languages 
a Java standard library is needed.

That's because the JVM specification itself relies on it.
For example, when trying to fetch from a null array reference, the spec states that the exception to throw is
`java/lang/NullPointerException`.

For these reasons, users should probably provide a Java standard library on their class path when running class files.
You'll have to provide one if you want to run the tests:
```bash
pytest std_lib=path/to/std/lib/jar_file.jar
``` 

So where to find one?

If you have a JDK installed there's usually a jar file at `path/of/java/installation/jre/lib/rt.jar`.
If it's not there, you can check the web for information regarding your particular installation.

But that's not ideal, there is a **better way**.

The problem is that traditional standard libraries, like open-JDK and the Oracle JDK, rely heavily
on native methods. And, as you might recall, this implementation doesn't support them.
This creates a high probability that your class files won't be able to execute even simple tasks.

I recommend the [GNU classpath project](https://www.gnu.org/software/classpath/), 
which is a standard library implementation that's specifically designed for alternative JVMs.
It's reliance on native functionality is minimal which makes it a great fit.

On the technical side, it's structured to with JVM implementation in mind. 
So a possible evolution for this project is to fully include it as pyjvm's standard library. 

Tip: If you're having trouble building GNU classpath on your machine try passing the --disable-jni flag
to the ./configure program, which disables the compilation of native methods. They're prone to build problems
and are irrelevant for a JVM that won't execute them anyway. 


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
 