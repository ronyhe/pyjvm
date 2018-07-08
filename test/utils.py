from jawa.constants import ConstantPool

from pyjvm.frame_locals import Locals
from pyjvm.instructions.instructions import InstructorInputs
from pyjvm.stack import Stack


class DefaultInputs(InstructorInputs):
    DEFAULTS = {
        'locals': lambda: Locals(5),
        'op_stack': lambda: Stack(),
        'constants': lambda: ConstantPool
    }

    def __init__(self, **kwargs):
        actual_args = dict()
        actual_args.update(kwargs)
        for key, default_factory in self.DEFAULTS.items():
            try:
                v = actual_args[key]
            except KeyError:
                v = default_factory()

            actual_args[key] = v
        super().__init__(**actual_args)
