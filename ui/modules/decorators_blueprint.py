#!/usr/bin/env python

"""The template of decorators. We use functools and *args, **kwargs (Idk why)"""

from functools import wraps


def decorator_name(f):
    @wraps(f)
    def wrap_func(*args, **kwargs):
        if not can_run:
            return "no function decorated"
        print "function is decorated"
        return f(*args, **kwargs)
    return wrap_func


@decorator_name
def f_needs_decoration():
    print "I need to be decorated"
    return 1


can_run = False
print(f_needs_decoration())

can_run = True
print(f_needs_decoration())
