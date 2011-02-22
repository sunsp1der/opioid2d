
import warnings

def deprecated(func):
    def wrapped(*arg, **kw):
        warnings.warn("method %s has been deprecated and will be removed in the next version of Opioid2D" % func.func_name, DeprecationWarning, 2)
        return func(*arg, **kw)
    return wrapped