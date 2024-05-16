import logging
from functools import wraps
from time import time

import numpy as np

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def timeit_once(func):
    @wraps(func)
    def wrapper(*args, **kw):
        t0 = time()
        result = func(*args, **kw)
        logger.info(f"{func.__name__}() TOOK {(time() - t0):.3f} seconds")
        return result

    return wrapper


def timeit(func):
    @wraps(func)
    def wrapper(*args, **kw):
        t0 = time()
        result = func(*args, **kw)
        wrapper.times.append(time() - t0)
        if len(wrapper.times) % 100 == 0:
            logger.info(
                f"{func.__name__}() averaged {np.average(wrapper.times):.3f} seconds over {len(wrapper.times)} calls"
            )
            wrapper.times = wrapper.times[:1000]  # 500 cutoff
        return result

    wrapper.times = []
    return wrapper
