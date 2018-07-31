"""Setup for using the py.test framework

The main function of this module is to provide a so-called test fixture for tests that need a standard library.
To use this a test function need to declare the parameter `std_loader` and the test runner will take care of the rest.

    .. code::

        def test_something(std_lib)
            pass

This uses the py.test fixture features with which I am not very familiar.
For more details see: https://docs.pytest.org/en/latest/example/simple.html

For performance reasons, the loader is only created once, so tests that use it should take care
to not change its mutable parts:
 - The statics dictionary for classes
 - The ConstantPool instance for classes

To address this issue in the long term -
the mutable parts of the loader should be extracted or have the ability to reset.

"""

import pytest

from pyjvm.core.class_loaders import TraditionalLoader

_STD_LOADER = None


@pytest.fixture
def std_loader(request):
    global _STD_LOADER
    if _STD_LOADER is None:
        _STD_LOADER = TraditionalLoader('')

    return _STD_LOADER
