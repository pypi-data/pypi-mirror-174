import time
from functools import wraps, partial
from typing import Callable
import logging

def time_def(func: Callable = None, 
            level:int =logging.DEBUG, 
            log_name: str=None) -> Callable:
    """
    This function is a decorator
    It will run the function the decorator is applied to, and return its result
    Printing the execution time

    eg.

    @time_it
    def time_max(A):
        return max(A)

    time_max([1,2,3,4,6]) # will return max value and print execution time

    """

    if func is None:
        return partial(time_def, level=level, log_name=log_name)
    
    log = None 
    if log_name is not None:
        log = logging.getLogger(log_name)
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        # storing time before function execution
        begin = time.time()

        r = func(*args, **kwargs) # exec the actual function

        # storing time after function execution
        end = time.time()

        elasped = end - begin

        if log:
            log.log(level, f" DEF {func.__name__} : TIME {elasped:.8f}")
        else:
            print(f" DEF {func.__name__} : TIME {elasped:.8f}")

        return r

    return wrapper
