
from Opioid2D import *

def pyempty(a, b):
    return 0

def pyfunc(a, b):
    a = a * 5
    b = b - a * 2
    c = a + b
    if a > b:
        c = c / 5
    return c

@o2dfunc(IntType,IntType,retvalue=IntType)
def vmfunc(a,b):
    return (
        a <= a * 5,
        b <= b - a * 2,
        c <= a + b,
        If(a > b).Then(
            c <= c / 5,
        ),
        Return(c),
        )

@o2dfunc(IntType,IntType,retvalue=IntType)
def vmempty(a,b):
    return (
        Return(0),
        )

if __name__=='__main__':
    from timeit import Timer
    t = Timer("pyfunc(12,34)", "from __main__ import pyfunc")
    t1 = t.timeit()
    t = Timer("pyempty(12,34)", "from __main__ import pyempty")
    t2 = t.timeit()
    print "Python func", t1-t2
    t = Timer("vmfunc(12,34)", "from __main__ import vmfunc")
    t1 = t.timeit()
    t = Timer("vmempty(12,34)", "from __main__ import vmempty")
    t2 = t.timeit()
    print "o2dfunc", t1-t2
