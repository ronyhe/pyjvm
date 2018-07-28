"""Setup for using the py.test framework

The main point is to add a command line argument for testing.
Namely a path to a Java Standard Library.
I don't know much about py.test internals, so this is copied almost verbatim from the py.test documentation.
See 
"""

import pytest

from pyjvm.model.class_loaders import TraditionalLoader


# noinspection SpellCheckingInspection
def pytest_addoption(parser):
    parser.addoption(
        "--std_lib", action="store", help="A path to a JAR file that contains the Java standard library"
    )


@pytest.fixture
def std_loader(request):
    path = request.config.getoption('--std_lib')
    if not path:
        raise Exception('Please supply --std_lib for proper testing ')
    return TraditionalLoader(path)
