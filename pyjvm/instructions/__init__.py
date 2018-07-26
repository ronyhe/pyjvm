""" A package that implements the JVM instructions and the dispatch mechanism used to access those implementations

The file instructions.py implements the dispatch mechanism and
some utilities that are shared across instruction implementations.

The file switches.py defines helper classes for the tableswitch and lookupswitch instructions.

Excluding those files, all other files in the package define `instructions.Instructor` instances and register them
to be called by instructions.py.

The instructions are divided into files according to the division that exists in section 7 of the JVM 8 spec,
"Opcode Mnemonics by Opcode".
See https://docs.oracle.com/javase/specs/jvms/se8/html/jvms-7.html

The exclusions to these rule are:
    - Unimplemented or no-op instructions reside in instructions.py.
      This includes the instructions under the "reserved" category.
    - The so called 'extended' instructions are variants of other instructions,
      so they reside in their semantically relevant location:
        - multianewarray in references.py
        - ifnull and ifnonnull in comparisons.py
        - goto_w in control.py
        - jsr_w, not implemented, as specified in instructions.py
"""
