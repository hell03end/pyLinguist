from collections import Callable
import unittest

from .config import Logger

logger = Logger(__name__)


class GenericTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        self._callback_called = False
        super(GenericTest, self).__init__(*args, **kwargs)

    def generic_callback(self, *args, **kwargs) -> None:
        self._callback_called = True


def assert_correct_import(import_func: Callable) -> Callable:
    def wrapper(*args, **kwargs) -> None:
        exceptions_happend = False
        try:
            import_func(*args, **kwargs)
        except ImportError as err:
            logger.debug(err)
            exceptions_happend = True
        assert not exceptions_happend
    return wrapper
