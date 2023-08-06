import time
from typing import Callable


def timeit(method: Callable) -> Callable:
    def timed(*args, **kw):
        if 'message' in kw:
            print(kw['message'])
            kw.pop('message')
        print(method.__name__, end="   ")
        start_time = time.time()
        result = method(*args, **kw)
        end_time = time.time()
        print(f'%2.2f s' % (end_time - start_time))
        print('-' * 20)
        return result

    return timed
