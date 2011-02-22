
import struct

from Opioid2D.public.opivm.opcodes import _opcodemap
import cOpioid2D as _c

class O2DCode(object):
    def __init__(self, cframe):
        self.code = cframe.code
        self.consts_f = cframe.consts_f
        self.consts_i = cframe.consts_i
        self.consts_v = cframe.consts_v
        self.consts_p = cframe.consts_p
        self.varcount_f = len(cframe.vars_f)
        self.varcount_i = len(cframe.vars_i)
        self.varcount_v = len(cframe.vars_v)
        self.varcount_p = len(cframe.vars_p)
        self.stack = cframe.max_stack
        
        self._init_c()
        self._frame = _c.ExecFrame(self._cObj)
        
    def __call__(self, *args):
        if len(args) != len(self.argspec):
            raise TypeError("incorrect number of arguments (expected %i got %i)" % (len(self.argspec), len(args)))
        #ef = _c.ExecFrame(self._cObj)
        ef = self._frame
        ef.restart()
        for a,t in zip(args,self.argspec):
            t().c_push(ef, a)
        ef.execute()
        if self.retvalue is not None:
            ret = self.retvalue().c_pop(ef)
        else:
            ret = None
        return ret
    
    def Call(self, *args):
        from Opioid2D.public.opivm.expressions import VMCall
        return VMCall(self, *args)
            
    def _init_c(self):
        c = self._cObj = _c.CodeObj()
        c.max_stack = self.stack
        c.varcount_f = self.varcount_f
        c.varcount_i = self.varcount_i
        c.varcount_v = self.varcount_v
        c.varcount_p = self.varcount_p
        c.init_code(self.code)
        c.init_const_f(len(self.consts_f))
        c.init_const_i(len(self.consts_i))
        c.init_const_v(len(self.consts_v))
        c.init_const_p(len(self.consts_p))
        for i,v in enumerate(self.consts_f):
            c.set_const_f(i, v)
        for i,v in enumerate(self.consts_i):
            c.set_const_i(i, v)
        for i,v in enumerate(self.consts_v):
            c.set_const_v(i, _c.Vec2(*v))
        for i,v in enumerate(self.consts_p):
            c.set_const_p(i, v._cObj)

class CompilerFrame(object):
    def __init__(self):
        self.consts_f = []
        self.consts_i = []
        self.consts_v = []
        self.consts_p = []
        self.vars_f = []
        self.vars_i = []
        self.vars_v = []
        self.vars_p = []

        self.stack = 0
        self.max_stack = 0

        self.code = ""

        self.debugout = False

    def compile(self, op):
        opc,param,stack,typ = op
        self.stack += stack
        self.max_stack = max(self.max_stack, self.stack)
        opnum,conv = _opcodemap[opc]
        conv = conv()
        if self.debugout:
            print "%-10s: %-20s (%10s)  (stack%+i) (cumul %i)" % (opc,conv.format(param),typ,stack,self.stack)
        param = conv.convert(self, param)
        bin = struct.pack("@BB", opnum, param)
        self.code += bin
        return bin
