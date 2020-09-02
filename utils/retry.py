#! /usr/bin/env python3
# coding: utf-8
# 一个可以捕捉错误并重试的封装
from functools import wraps, partial


def wrap_caller(caller):
    def decor(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            return caller(f, *args, **kwargs)

        return wrapper

    return decor


def __retry_internal(
    f, exceptions=Exception, tries=-1,
):
    _tries = tries
    while _tries:
        try:
            return f()
        except exceptions:
            _tries -= 1
            if not _tries:
                raise


def retry(exceptions=Exception, tries=-1):
    """
    a decorator to retry call the function if some particular exceptions happened

    Args:
        exceptions: exceptions you want to catch, can be a tuple, Exception by default
        tries: times you want to retry,never stop by default
    """

    @wrap_caller
    def retry_decorator(f, *fargs, **fkwargs):
        args = fargs if fargs else list()
        kwargs = fkwargs if fkwargs else dict()

        return __retry_internal(partial(f, *args, **kwargs), exceptions, tries)

    return retry_decorator


@retry()
def t(a):
    print(a)
    # a/0


print("function running")
t(11)
