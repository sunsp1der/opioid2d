
__all__ = [
    "BoolType",
    "IntType",
    "FloatType",
    "VectorType",
    "SpriteType",
    ]

_tcodemap = {}

import cOpioid2D as _c

class TypeMeta(type):
    def __init__(self, *arg, **kw):
        type.__init__(self, *arg, **kw)
        self._build_map()
    
    def _build_map(self):
        self.props = dict(self.prop_list)
        m = self.methods = {}
        for name, args, ret in self.method_list:
            lst = m.setdefault(name, [])
            lst.append((args,ret))
        _tcodemap[self.typecode] = self
    
    def __str__(self):
        return self.__name__
    __repr__ = __str__

class Type(object):
    __metaclass__ = TypeMeta

    typecode = "?"
    varcode = "p"
    prop_list = []
    method_list = []

    def coercion_ops(self, other):
        return None


class BoolType(Type):
    stacksize = _c.get_int_size()
    typecode = "b"
    varcode = "i"
    default = False

    def coercion_ops(self, other):
        if other is IntType:
            return []
        
    def c_push(self, f, p):
        f.pushi(p)
        
    def c_pop(self, f):
        return bool(f.popi())
        
    def get_var(self, p):
        return bool(p)

class IntType(Type):
    stacksize = _c.get_int_size()
    typecode = "i"
    varcode = "i"
    default = 0
    
    def coercion_ops(self, other):
        from Opioid2D.public.opivm.expressions import F2I
        if other is FloatType:
            return F2I()._get_expr_ops()
        if other is BoolType:
            return []
        
    def c_push(self, f, p):
        f.pushi(p)
        
    def c_pop(self, f):
        return f.popi()
        
    def get_var(self, p):
        return int(p)

class FloatType(Type):
    stacksize = _c.get_float_size()
    typecode = "f"
    varcode = "f"
    default = 0.0
    
    def coercion_ops(self, other):
        from Opioid2D.public.opivm.expressions import I2F
        if other is IntType:
            return I2F()._get_expr_ops()

    def c_push(self, f, p):
        f.pushf(p)
            
    def c_pop(self, f):
        return f.popf()

    def get_var(self, p):
        return float(p)

#class StringType(Type):
#    stacksize = 
#    typecode = "p"

class VectorValue(Type):
    stacksize = FloatType.stacksize*2
    typecode = "w"
    varcode = "v"
    default = (0,0)
    
    def c_push(self, f, p):
        x,y = p
        f.pushf(x)
        f.pushf(y)
        
    def c_pop(self, f):
        from Opioid2D.public.Vector import Vector
        y = f.popf()
        x = f.popf()
        return Vector(x,y)

    def get_var(self, f, p):
        return _c.Vec2(*p)

    def coercion_ops(self, t):
        if t is VectorType:
            from Opioid2D.public.opivm.opcodes import opcode
            return [
                opcode("p2vec", None, VectorValue, stack=-VectorType.stacksize+VectorValue.stacksize),
                ]


class VectorType(Type):
    stacksize = _c.get_ptr_size()
    typecode = "v"
    default = (0,0)
    
    prop_list = [
        ("x", FloatType),
        ("y", FloatType),
        ("length", FloatType),
        ("direction", FloatType),
        ]
    
    def coercion_ops(self, t):
        if t is VectorValue:
            from Opioid2D.public.opivm.opcodes import opcode
            return [
                opcode("vec2p", None, VectorType, stack=VectorType.stacksize-VectorValue.stacksize),
                ]
    
    def c_push(self, f, p):
        f.pushv(_c.Vec2(*p))
        
    def c_pop(self, f):
        from Opioid2D.public.Vector import Vector
        v = f.popv()
        return Vector(v.x,v.y)
        
    def get_var(self, f, p):
        return _c.Vec2(*p)

VectorType.method_list = [
        ("set", [FloatType,FloatType], None),
        ("set", [VectorType], None),
        ("add", [FloatType,FloatType], None),
        ("add", [VectorType], None),
        ("sub", [FloatType,FloatType], None),
        ("sub", [VectorType], None),
        ("mul", [FloatType], None),
        ("mul", [FloatType,FloatType], None),
        ("mul", [VectorType], None),
        ("div", [FloatType], None),
        ("div", [FloatType,FloatType], None),
        ("div", [VectorType], None),
        ]
VectorType._build_map()

class SpriteType(Type):
    stacksize = _c.get_ptr_size()
    typecode = "p"
    default = 0
    
    prop_list = [
        ("position", VectorType),
        ("velocity", VectorType),
        ("acceleration", VectorType),
        ("friction", FloatType),
        ("rotation", FloatType),
        ("rotation_speed", FloatType),
        ("scale", VectorType),
        ("world_position", VectorValue),
        
        ]

    method_list = [
        ("delete", (), None),
        ]
    
    def c_push(self, f, p):
        from Opioid2D.public.Sprite import Sprite
        if isinstance(p, Sprite):
            f.pushp(int(p._cObj.this))
        else:
            raise TypeError
        
    def c_pop(self, f):
        p = f.popSprite()
        from Opioid2D.internal.objectmgr import ObjectManager
        p = ObjectManager.c2py(p)
        return p
        
    def get_var(self, p):
        from Opioid2D.public.Sprite import Sprite
        pass

_typemap = {
    int: IntType,
    float: FloatType,
#    str: StringType,
    bool: BoolType,
    }
