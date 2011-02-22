
__all__ = [
    "For",
    "If",
    "Range",
    ]

import sys, os
from Opioid2D.public.opivm.opcodes import _opmap, opcode
from Opioid2D.public.opivm.types import *
from Opioid2D.public.opivm.types import _typemap, _tcodemap, VectorValue

def _get_ops(expr):
    from Opioid2D.public.Vector import Vector
    from Opioid2D.public.Sprite import Sprite
    from Opioid2D.public.opivm.compiler import O2DCode
    
    if isinstance(expr, Expr):
        return expr._get_expr_ops()
    elif isinstance(expr, bool):
        return [
            opcode("consti", int(expr), BoolType, BoolType.stacksize)
            ]
    elif isinstance(expr, tuple):
        if len(expr) == 2:
            for x in expr:
                if isinstance(x, Expr):
                    return BuildVec(*expr)._get_expr_ops()
            return [
                opcode("constv", expr, VectorValue, VectorValue.stacksize)
                ]
        else:
            raise TypeError("can't use tuple of size %i as a constant" % len(expr))
    elif isinstance(expr, Vector):
        return [
            opcode("constv", expr, VectorValue, VectorValue.stacksize)
            ]
    elif isinstance(expr, Sprite):
        const_type = SpriteType
    else:
        try:
            const_type = _typemap[type(expr)]
        except KeyError:
            raise TypeError("can't use the constant %r in o2d expressions" % expr)
    return [
        opcode("const"+const_type.typecode, expr, const_type, const_type.stacksize)
        ]

def _frame2tb(f):
    ## temporarily disabled
    return []
    
    lines = []
    while f is not None:
        fn = f.f_code.co_filename
        ln = f.f_lineno
        mn = f.f_code.co_name
        if os.path.join("idlelib","PyShell.py") in fn:
            break
        try:
            src = open(fn).read().split("\n")[ln-1].strip()
        except:
            src = None
        lines.append((fn,ln,mn,src))
        f = f.f_back
    lines.reverse()
    return lines

       
class Expr(object):
    def __new__(cls, *arg, **kw):
        self = object.__new__(cls, *arg, **kw)
        self._tb = _frame2tb(sys._getframe(1))
        return self
    
    def _get_expr_ops(self):
        raise "invalid expr", self.__class__

    def _get_stmt_ops(self):
        return self._get_expr_ops()
    
    def __getattr__(self, name):
        return PropertyOp(self, name)

    def __eq__(self, other):
        return CmpOp("eq", self, other)

    def __ne__(self, other):
        return CmpOp("ne", self, other)

    def __lt__(self, other):
        return CmpOp("lt", self, other)

    def __le__(self, other):
        return CmpOp("le", self, other)

    def __gt__(self, other):
        return CmpOp("gt", self, other)

    def __ge__(self, other):
        return CmpOp("ge", self, other)

    def __neg__(self):
        return UnaryOp("neg", self)

    def __add__(self, other):
        return BinaryOp("add", self, other)

    def __sub__(self, other):
        return BinaryOp("sub", self, other)

    def __div__(self, other):
        return BinaryOp("div", self, other)

    def __mul__(self, other):
        return BinaryOp("mul", self, other)

    def __radd__(self, other):
        return BinaryOp("add", other, self)

    def __rsub__(self, other):
        return BinaryOp("sub", other, self)

    def __rdiv__(self, other):
        return BinaryOp("div", other, self)

    def __rmul__(self, other):
        return BinaryOp("mul", other, self)

    def __nonzero__(self, other):
        return UnaryOp("not", self)


class VarRef(Expr):
    def __init__(self, name, type=None):
        self._name = name
        self._type = type

    def _get_expr_ops(self):
        if self._type is None:
            raise SyntaxError("uninitialized variable: %s" % self._name)
        return [
            opcode("pushvar"+self._type.varcode, self._name, self._type, self._type.stacksize)
            ]
        
    def _get_stmt_ops(self):
        return []

class BinaryOp(Expr):
    def __init__(self, op, a, b):
        self._op = op
        self._a = a
        self._b = b

    def _get_expr_ops(self):
        a = _get_ops(self._a)
        b = _get_ops(self._b)
        a_type = a[-1][-1]
        b_type = b[-1][-1]
        if a_type is VectorValue:
            a.extend(VectorType().coercion_ops(VectorValue))
            a_type = VectorType
        if b_type is VectorValue:
            b.extend(VectorType().coercion_ops(VectorValue))
            b_type = VectorType
        if b_type is VectorType and a_type is not VectorType:
            a_type,b_type = b_type,a_type
            a,b = b,a
            
        codes = a_type.typecode + b_type.typecode
        op = self._op
        opmap = _opmap[op]
        try:
            coercions = opmap[codes]
        except KeyError:
                raise TypeError("invalid types %s and %s for operator %r" % (a_type,b_type,op))
        if coercions is not None:            
            coertype = _tcodemap[coercions[0]]
            if coertype is not a_type:
                a.extend(coertype().coercion_ops(a_type))
                a_type = coertype
            coertype = _tcodemap[coercions[1]]
            if coertype is not b_type:
                b.extend(coertype().coercion_ops(b_type))
                b_type = coertype
                
        typecode = a_type.typecode + b_type.typecode

        rt = self._get_returntype(a_type)
        if rt is VectorType:
            rt = VectorValue

        stack = -2 * a_type.stacksize + rt.stacksize
        ops = a + b
        ops.append(
            opcode("op_"+self._op+typecode, None, rt, stack)
            )
        return ops

    def _get_returntype(self, t):
        return t

class CmpOp(BinaryOp):
    
    def _get_stmt_ops(self):
        if self._op == 'le':
            return AssignOp(self._a, self._b)._get_stmt_ops()
        return self._get_expr_ops()

    def _get_returntype(self, t):
        return BoolType
    
class I2F(Expr):
    def _get_expr_ops(self):
        return [
            opcode("i2f", None, FloatType, FloatType.stacksize-IntType.stacksize)
            ]

class F2I(Expr):
    def _get_expr_ops(self):
        return [
            opcode("f2i", None, IntType, IntType.stacksize-FloatType.stacksize)
            ]
        
class BuildVec(Expr):
    def __init__(self, x, y):
        self._vec = (x,y)
    
    def _get_expr_ops(self):
        ops = []
        for p in self._vec:
            pops = _get_ops(p)
            pt = pops[-1][-1]
            if pt is not FloatType:
                co = FloatType().coercion_ops(pt)
                if co is None:
                    raise TypeError("illegal type to building vector value: %s" % pt)
                pops.extend(co)
            ops.extend(pops)
        opc,param,stack,typ = ops[-1]
        ops[-1] = opc,param,stack,VectorValue
        return ops
        
class VMCall(Expr):
    def __init__(self, code, *args):
        self._code = code
        self._args = args
        
    def _get_ops(self, expr=False):
        code = self._code
        # push params
        ops = []
        stack = 0
        argsize = 0
        for typ,arg in zip(code.argspec, self._args):
            argsize += typ.stacksize
            argops = _get_ops(arg)
            t = argops[-1][-1]
            if t is not typ:
                co = typ().coercion_ops(t)
                if co is None:
                    raise TypeError("invalid argument for vmcall (expected %s got %s)" % (typ, t))
                argops.extend(co)
            ops.extend(argops)            
        # vmcall opcodes
        stack = -argsize
        rt = code.retvalue
        if rt:
            rtstack = rt.stacksize
            stack += rt.stacksize
        else:
            rtstack = 0
        ops.append(
            opcode("consti", rtstack, stack=IntType.stacksize)
            )
        ops.append(
            opcode("constp", code, None, stack=SpriteType.stacksize)
            )
        ops.append(
            opcode("vmcall", argsize, rt, stack-IntType.stacksize-SpriteType.stacksize)
            )
        # pop result
        if not expr and rt:
            ops.append(
                opcode("pop", rtstack, None, -rtstack)
                )
        return ops
    
    def _get_expr_ops(self):
        return self._get_ops(expr=True)
    
    def _get_stmt_ops(self):
        return self._get_ops(expr=False)

class AssignOp(Expr):
    def __init__(self, target, value):
        self._target = target
        self._value = value

    def _get_expr_ops(self):
        raise SyntaxError("using assignment in an expression")

    def _get_stmt_ops(self):
        if isinstance(self._target, PropertyOp):
            self._target._set(self._value)
            return self._target._get_stmt_ops()
        elif isinstance(self._target, VarRef):
            ops = _get_ops(self._value)
            vt = ops[-1][-1]
            if self._target._type is None:
                self._target._type = vt
            elif vt is not self._target._type:
                co = self._target._type().coercion_ops(vt)
                if co is None:
                    raise Exception("cannot convert %s to %s" % (vt, self._target._type))
                ops.extend(co)
            ops.append(
                opcode("setvar"+self._target._type.varcode, self._target._name, None, -self._target._type.stacksize)
                )
            return ops
        raise Exception("assignment to invalid target")
        

class UnaryOp(Expr):
    def __init__(self, op, a):
        self._op = op
        self._a = a

    def _get_expr_ops(self):
        ops = _get_ops(self._a)
        vt = ops[-1][-1]
        if vt is VectorType:
            rt = VectorValue
        elif vt is VectorValue:
            ops.extend(VectorType().coercion_ops(VectorValue))
            vt = VectorType
            rt = VectorValue
        else:
            rt = vt
        ops.append(
            opcode("op_"+self._op+vt.typecode, None, rt, rt.stacksize-vt.stacksize)
            )
        return ops


class PropertyOp(Expr):
    def __init__(self, target, name):
        self._target = target
        self._name = name
        self._args = None
        self._value = None

    def __call__(self, *args):
        self._args = args
        return self

    def _set(self, value):
        self._value = value

    def _get_expr_ops(self):
        return self._get_ops(True)
    
    def _get_stmt_ops(self):
        return self._get_ops(False)

    def _get_ops(self, expr):
        target_ops = _get_ops(self._target)
        tt = target_ops[-1][-1]
        if tt is VectorValue:
            target_ops.extend(VectorType().coercion_ops(VectorValue))
        if self._value is not None:
            if expr:
                raise SyntaxError("illegal property assignment in an expression")
            try:
                tt = target_ops[-1][-1]
                rt = tt.props[self._name]
            except KeyError:
                raise AttributeError("%s object has no property called %r" % (tt, self._name))
            ops =_get_ops(self._value)
            vt = ops[-1][-1]
            if vt is not rt:
                co = rt().coercion_ops(vt)
                if co is None:
                    raise TypeError("cannot assign %s to property %s.%s (requires %s)" % (vt, tt, self._name, rt))
                vt = co[-1][-1]
                ops.extend(co)
            ops.extend(target_ops)
            code = "setprop"
            if tt is VectorType:
                code += "v"
            ops.append(
                opcode(code, (tt,self._name), None, -vt.stacksize-tt.stacksize)
                )
            if type(self._target) is VarRef and self._target._type is VectorValue:
                ops.extend(
                    AssignOp(self._target, LastVec())._get_stmt_ops(),
                    )
        elif self._args is not None:
            ops = []
            try:
                tt = target_ops[-1][-1]
                ol_lst = tt.methods[self._name]
#                at,rt = tt.methods[self._name]
            except KeyError:
                raise AttributeError("%s object has no method called %r" % (tt, self._name))
            
            for ol_idx, (at,rt) in enumerate(ol_lst):
                if len(self._args) != len(at):
                    continue
                stack = 0
                argops = []
                for a,t in zip(self._args,at):
                    argops.extend(_get_ops(a))
                    argt = argops[-1][-1]
                    if argt is not t:
                        co = t().coercion_ops(argt)
                        if co is None:
                            break
                        argops.extend(co)
                    stack -= t.stacksize
                else:
                    break
            else:
                argtypes = []
                for a in self._args:
                    argt = _get_ops(a)[-1][-1]
                    argtypes.append(argt)
                arglist = ", ".join(str(a) for a in argtypes)
                raise TypeError("cannot call %s.%s with parameters (%s)" % (tt,self._name,argtypes))
                
            ops.extend(argops)
                
##            ops.append(
##                opcode("args", len(self._args), None, stack)
##                )
            if rt is None:
                rtstack = 0
            else:
                rtstack = rt.stacksize
            ops.extend(target_ops)
            code = "metcall"
            if tt is VectorType:
                code += "v"
            ops.append(
                opcode(code, (tt,self._name,ol_idx), rt, rtstack-tt.stacksize-stack)
                )
            if type(self._target) is VarRef and self._target._type is VectorValue:
                ops.extend(
                    AssignOp(self._target, LastVec())._get_stmt_ops(),
                    )            
            if not expr and rt is not None:
                ops.append(
                    opcode("pop", rt.stacksize, None, -rt.stacksize)
                    )
        else:
            ops = target_ops
            try:
                tt = ops[-1][-1]
                rt = tt.props[self._name]
            except KeyError:
                raise AttributeError("%s object has no property called %r" % (tt, self._name))
            if not expr:
                return []
            code = "getprop"
            if tt is VectorType:
                code += "v"
            ops.append(
                opcode(code, (tt,self._name), rt, rt.stacksize-tt.stacksize)
                )
        return ops

class LastVec(Expr):
    def _get_expr_ops(self):
        return [
            opcode("lastvec", None, VectorValue, VectorValue.stacksize),
            ]

class If(Expr):
    def __init__(self, cond):
        self.cond = cond
        self.then = []
        self.elses = []
        self.elifs = []
        self.parent = None

    def Then(self, *statements):
        self.then = statements
        return self

    def _Elif(self, cond):
        l = If(cond)
        l.parent = self
        self.elifs.append(l)
        return l

    def Else(self, *statements):
        self.elses = statements
        return self

    def _get_stmt_ops(self):
        ops = _get_ops(self.cond)
        if self.parent is not None:
            return self.parent._get_stmt_ops()
        elses = []
        for t in self.elses:
            elses.extend(t._get_stmt_ops())
        then = []
        for t in self.then:
            then.extend(t._get_stmt_ops())
        if elses:
            then.append(
                opcode("jump", len(elses))
                )
        ops.append(
            opcode("ifjump", len(then), None, -BoolType.stacksize)
            )
        ops.extend(then)
        ops.extend(elses)
        return ops

class Range(Expr):
    def __init__(self, start=0, end=None, step=1):
        if end is None:
            self._start = 0
            self._end = start
        else:
            self._start = start
            self._end = end
        self._step = step


    def __contains__(self, var):
        if not isinstance(var, VarRef):
            raise SyntaxError("invalid loop variable for For-loop")
        self._var = var
        return self


class For(Expr):
    def __init__(self, rng):
        try:
            if rng._op != "le":
                (1).foo
            self._var = rng._a
            rng = rng._b
            if self._var._type is None:
                self._var._type = IntType
            elif self._var._type is not IntType:
                raise TypeError("non-integer loop variable %s" % self._var._name)
        except AttributeError:
            raise SyntaxError("invalid For-loop")
        self._start = rng._start
        self._end = rng._end
        self._body = None

    def Do(self, *statements):
        self._body = statements
        return self

    def _get_stmt_ops(self):
        if not self._body:
            return []
        start = _get_ops(self._start)
        end = _get_ops(self._end)
        st = start[-1][-1]
        et = end[-1][-1]
        if st is not IntType:
            co = IntType().coerce_ops(st)
            if co is None:
                raise TypeError("invalid type for loop range: %s" % st)
            start += co
        if et is not IntType:
            co = IntType().coerce_ops(et)
            if co is None:
                raise TypeError("invalid type for loop range: %s" % et)
            end += co
        body = []
        for s in self._body:
            body.extend(s._get_stmt_ops())
        ops = start + end
        ops.append(
            opcode("initfor", self._var._name, None, -2 * IntType.stacksize),
            )
        ops.append(
            opcode("loop", len(body))
            )
        ops.extend(body)
        return ops

def Return(typ):
    class TypedReturn(Expr):
        def __init__(self, value=None):
            self._value = value
            
        def _get_stmt_ops(self):
            value = self._value
            if typ is None and value is not None:
                raise TypeError("function can't return any values")
            if typ is not None and value is None:
                raise TypeError("function must return a value")            
            ops = []
            if value is not None:
                ops.extend(_get_ops(value))
            if typ is not None:
                rt = ops[-1][-1]
                if rt is not typ:
                    co = typ().coercion_ops(rt)
                    if co is None:
                        raise TypeError("can't return a value of type %s" % rt)
                    ops.extend(co)
            ops.append(
                opcode("exit")
                )
            return ops
    return TypedReturn
