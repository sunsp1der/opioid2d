
__all__ = [
    "Vector",
    ]

import cOpioid2D as _c

class Vector(object):
    def __init__(self, x=0, y=0, direction=None, length=None):
        if direction is not None:
            self._cObj = _c.Vec2(direction,length).rad2xy()
            self._cObj.thisown = True
        else:
            self._cObj = _c.Vec2(x,y)
        
    def get_x(self):
        return self._cObj.x
    def set_x(self, x):
        self._cObj.x = x
    x = property(get_x, set_x)
    
    def get_y(self):
        return self._cObj.y
    def set_y(self, y):
        self._cObj.y = y
    y = property(get_y, set_y)
    
    def __getitem__(self, i):
        if i == 0:
            return self._cObj.x
        elif i == 1:
            return self._cObj.y
        else:
            raise IndexError("invalid index for Vector: %r" % i)
    def __setitem__(self, i, value):
        if i == 0:
            self._cObj.x = value
        elif i == 1:
            self._cObj.y = value
        else:
            raise IndexError("invalid index for Vector: %r" % i)
    def __iter__(self):
        c = self._cObj
        yield c.x
        yield c.y

    def get_direction(self):
        return self._cObj.direction()
    def set_direction(self, value):
        self._cObj.set_direction(value)
    direction = property(get_direction, set_direction)
    
    def get_length(self):
        return self._cObj.length()
    def set_length(self, value):
        self._cObj.set_length(value)
    length = property(get_length, set_length)
    
    def get_radial(self):
        v = self._cObj.xy2rad()
        v.thisown = True
        return v.x,v.y
    def set_radial(self, (dir,len)):
        self._cObj.set_radial(dir,len)
    radial = property(get_radial, set_radial)
    
    def dot(self, other):
        return self.x * other[0] + self.y * other[1]
    
    def angle(self, other):
        return self._cObj.angle(other._cObj)
    
    def __add__(self, other):
        c = self._cObj
        return Vector(c.x + other[0], c.y + other[1])
    __radd__ = __add__
    def __iadd__(self, other):
        c = self._cObj
        c.set(c.x + other[0], c.y + other[1])
        return self
        
    def __sub__(self, other):
        c = self._cObj
        return Vector(c.x - other[0], c.y - other[1])
    def __rsub__(self, other):
        c = self._cObj
        return Vector(other[0] - c.x, other[1] - c.y)
    def __isub(self, other):
        c = self._cObj
        c.set(c.x - other[0], c.y - other[1])
        return self
    
    def __mul__(self, other):
        c = self._cObj
        if isinstance(other, (int, long, float)):
            return Vector(c.x * other, c.y * other)
        return Vector(c.x * other[0], c.y * other[1])
    __rmul__ = __mul__
    def __imul__(self, other):
        c = self._cObj
        if isinstance(other, (int, long, float)):
            c.set(c.x * other, c.y * other)
        else:
            c.set(c.x * other[0], c.y * other[1])
        return self
    
    def __div__(self, other):
        c = self._cObj
        if isinstance(other, (int, long, float)):
            return Vector(c.x / other, c.y / other)
        return Vector(c.x / other[0], c.y / other[1])
    def __rdiv__(self, other):
        c = self._cObj
        if isinstance(other, [int, long, float]):
            raise TypeError
        return Vector(other[0] / c.x, other[1] / c.y)
    def __idiv__(self, other):
        c = self._cObj
        if isinstance(other, [int, long, float]):
            c.set(c.x / other, c.y / other)
        else:
            c.set(c.x / other[0], c.y / other[1])
        return self
        
    def __str__(self):
        return "Vector(%.3f, %.3f)" % (self.x, self.y)
        
class VectorReference(Vector):
    def __init__(self, cobj, owner):
        self._cObj = cobj
        # Save the reference to the owner in order to keep the Python object alive.
        # Otherwise the _c.Vec2 object might get invalidated.
        self._owner = owner 