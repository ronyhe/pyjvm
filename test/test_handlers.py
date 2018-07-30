from pyjvm.model.jvm_class import ExceptionHandler, Handlers
from test.utils import NPE_CLASS_NAME

HANDLER = ExceptionHandler(
    start_pc=0,
    end_pc=2,
    handler_pc=3,
    catch_type=NPE_CLASS_NAME
)


def test_handlers():
    handler = HANDLER

    assert handler.relevant_to_pc(handler.start_pc)
    assert not handler.relevant_to_pc(2)

    handlers = Handlers([handler])
    assert handlers.find_handlers(handler.start_pc) == (handler,)
