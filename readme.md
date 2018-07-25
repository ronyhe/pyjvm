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
- It does not obey JVM the arithmetic overflow rules of the spec. Instead it uses python math operations directly.
- It does little to no verification of class files
- It does little to no verification of instruction preconditions
- It rarely complies with the exceptions that instructions should throw

Addressing these issues should not prove very difficult. Others are welcome to tackle them.
In fact, this might prove a useful didactic task for students of various advanced topics.
 
### Acknowledgements
There are dozens of people I learned from and dozens of tools I use every day. 
Too many to list here, so I'll point out two that were especially relevant in this project. 
I'd like to thank the creators and maintainers of:

- The [JVM specification]((https://docs.oracle.com/javase/specs/jvms/se8/html/index.html)) (Oracle and previously Sun)
- The [jawa python library](https://github.com/TkTech/Jawa) (TkTech)
 