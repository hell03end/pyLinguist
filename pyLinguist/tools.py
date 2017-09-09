'''Common functions'''

from collections import Callable
from threading import Thread


def async_run(f: Callable) -> Callable:
    '''Run functions in separate threads'''
    def wrapper(*args, **kwargs) -> None:
        thread = Thread(target=f, args=args, kwargs=kwargs)
        thread.start()
    return wrapper
