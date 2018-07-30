from jawa.attributes.code import CodeException
from jawa.cf import ClassFile

from pyjvm.model.jvm_class import ExceptionHandler, Handlers
from pyjvm.utils.jawa_conversions import convert_class_file, key_from_method
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


def test_conversion():
    cf = ClassFile.create('some_class')
    exception_name = 'some_name'
    exception_class = cf.constants.create_class(exception_name)
    method = cf.methods.create('some_method', '()V', code=True)
    method.code.assemble([])

    method.code.exception_table.append(CodeException(
        start_pc=0,
        end_pc=2,
        handler_pc=3,
        catch_type=exception_class.index
    ))

    jvm_class = convert_class_file(cf)
    method = jvm_class.methods[key_from_method(method)]
    handlers = method.exception_handlers.handlers
    assert len(handlers) == 1
    handler = handlers[0]
    assert handler.catch_type == exception_name
