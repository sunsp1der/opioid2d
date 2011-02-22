
__all__ = [
    "o2dfunc",
    ]

import inspect, sys, traceback, os, new

import Opioid2D.public.opivm.types as opitypes
import Opioid2D.public.opivm.expressions as opiexpr
from Opioid2D.public.opivm.compiler import CompilerFrame, O2DCode
from Opioid2D.public.opivm.expressions import VarRef
from Opioid2D.public.opivm.opcodes import opcode

class o2dfunc(object):
    def __init__(self, *types, **opts):
        self.types = list(types)
        for i,t in enumerate(self.types):
            if t is opitypes.VectorType:
                self.types[i] = opitypes.VectorValue
        self.opts = opts

    def __call__(self, func):
        retvalue = self.opts.get("retvalue", None)
        if retvalue is opitypes.VectorType:
            retvalue = opitypes.VectorValue
        fargs = inspect.getargs(func.func_code)[0]
        args = [VarRef(arg,typ) for arg,typ in zip(fargs,self.types)]
        code = func.func_code
        names = code.co_names
        dct = {}
        dct.update(func.func_globals)
        for n in names:
            if n in opiexpr.__all__:
                dct[n] = getattr(opiexpr, n)
            elif n not in func.func_globals:
                dct[n] = VarRef(n)
                
        dct["Return"] = opiexpr.Return(retvalue)
                                
        newfunc = new.function(code, dct, func.func_name, closure=func.func_closure)
        #args = dict((arg,VarRef(arg,typ)) for arg,typ in zip(args,self.types))
        statements = newfunc(*args)
        ops = []
        for a in reversed(args):
            ops.append(
                opcode("setvar"+a._type.varcode, a._name, None, -a._type.stacksize)
                )            
        for s in statements:
            try:
                ops.extend(s._get_stmt_ops())
            except:
                t,v,tb = sys.exc_info()
                for l in traceback.format_list(s._tb):
                    sys.stderr.write(l)
                for l in traceback.format_exception_only(t,v):
                    sys.stderr.write(l)
                tb = None
                raise
                return
        if not ops or ops[-1][0] != "exit":
            if retvalue is not None:
                ops.extend(opiexpr._get_ops(retvalue.default))
            ops.append(opcode("exit"))
        cc = CompilerFrame()
        cc.stack = sum(a._type.stacksize for a in args)
        cc.max_stack = cc.stack
        cc.debugout = self.opts.get("debugout", False)
        for op in ops:
            cc.compile(op)
        if cc.debugout:
            print "max. stack usage: %i bytes" % cc.max_stack
            print cc.__dict__
        code = O2DCode(cc)
        code.retvalue = retvalue
        code.argspec = self.types
        return code
