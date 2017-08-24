from collections import Callable

from .config import logger


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
