#!/usr/bin/env python

"""This is a test function with decorators with sugar syntax"""


def a_new_decorator(f):
    def wrap_func(*args, **kwargs):
        print "happens BEFORE"
        f()
        print "happens AFTER"
    return wrap_func


@a_new_decorator
def f_needs_decoration():
    print "I need to be decorated"


f_needs_decoration()
print f_needs_decoration.__name__
