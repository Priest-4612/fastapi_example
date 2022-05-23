from functools import wraps


def coroutine(coro):
    @wraps(coro)
    def coroinit(*args, **kwargs):
        fn = coro(*args, **kwargs)
        next(fn)
        return fn
    return coroinit
