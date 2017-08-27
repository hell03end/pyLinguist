from collections import Callable
import unittest

from .config import logger


class GenericTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        self._callback_called = False
        super(GenericTest, self).__init__(*args, **kwargs)

    def generic_callback(self, *args, **kwargs) -> None:
        self._callback_called = True

    def assert_exception_happend(self, func: Callable, exception: Exception,
                                 *args, **kwargs) -> bool:
        try:
            func(*args, **kwargs)
            return False
        except exception as err:
            logger.debug(err)
            return True


def assert_correct_import(import_func: Callable):
    def wrapper(*args, **kwargs):
        exceptions_happend = False
        try:
            import_func(*args, **kwargs)
        except ImportError as err:
            logger.debug(err)
            exceptions_happend = True
        assert not exceptions_happend
    return wrapper
