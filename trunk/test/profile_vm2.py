
from Opioid2D import *

def pyempty():
    pass

def pyfunc():    
    a = Vector(12,34)
    b = Vector(45,67)
    c = a + b
    d = a * 10
    x = a.x
    y = a.y

@o2dfunc()
def vmfunc():
    return (
        a <= (12,34),
        b <= (45,67),
        c <= a + b,
        d <= a * 10,
        x <= a.x,
        y <= a.y,
        )

@o2dfunc()
def vmempty():
    return ()

if __name__=='__main__':
    from timeit import Timer
    t = Timer("pyfunc()", "from __main__ import pyfunc")
    t1 = t.timeit()
    t = Timer("pyempty()", "from __main__ import pyempty")
    t2 = t.timeit()
    print "Python func", t1-t2
    t = Timer("vmfunc()", "from __main__ import vmfunc")
    t1 = t.timeit()
    t = Timer("vmempty()", "from __main__ import vmempty")
    t2 = t.timeit()
    print "o2dfunc", t1-t2
