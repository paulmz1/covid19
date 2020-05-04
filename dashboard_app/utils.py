from functools import wraps
from time import time
import logging
# https://codereview.stackexchange.com/questions/169870/decorator-to-measure-execution-time-of-a-function


def init_logger():
    logging.basicConfig(level=logging.DEBUG, format='%(message)s             (%(asctime)s | %(name)s | %(levelname)s)')  #


def getLogger(name):
    return logging.getLogger(name)


log = getLogger(__name__)


def timer(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        start = time()
        result = f(*args, **kwargs)
        elapsed = time() - start

        log.info(f'def {f.__module__}.{f.__name__}() took {elapsed:.3f}s.' +
                 (f' {(1/elapsed):.2f}s^-1.' if elapsed > 0 else ''))
        return result
    return wrapper


@timer
def long_loop(n):
    for i in range(n):
        a = i^2

if __name__ == '__main__':
    init_logger()
    long_loop(50000)

