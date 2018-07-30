from pyjvm.core.actions import Invoke
from pyjvm.core.jvm_class import MethodKey
from pyjvm.core.machine import Machine
from test.utils import NPE_CLASS_NAME


def test_method_from_super_class(std_loader):
    instance = std_loader.default_instance(NPE_CLASS_NAME)
    action = Invoke(
        NPE_CLASS_NAME,
        MethodKey(
            'toString',
            '()Ljava/lang/String;'
        ),
        [instance]
    )
    machine = Machine(std_loader)
    machine.act(action)
    assert machine.frames.peek().method_name == 'toString'
