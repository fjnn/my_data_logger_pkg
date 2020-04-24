#!/usr/bin/env python

"""This is a test function with decorators with sugar syntax and functools. We use functools instead of *args, **kwargs"""

from functools import wraps


def a_new_decorator(f):
    @wraps(f)
    def wrap_func():
        print "happens BEFORE"
        f()
        print "happens AFTER"
    return wrap_func


@a_new_decorator
def f_needs_decoration():
    print "I need to be decorated"


f_needs_decoration()
print f_needs_decoration.__name__
