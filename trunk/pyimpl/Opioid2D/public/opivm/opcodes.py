4
def opcode(name, value=None, type=None, stack=0):
    return (name, value, stack, type)

_std = {
    'ii':None,
    'ff':None,
    'if':'ff',
    'fi':'ff',
    }

_stdeq = {
    'ii':None,
    'ff':None,
    'if':'ff',
    'fi':'ff',
    'vv':None,
    }

_vecsca = {
    'ii':None,
    'ff':None,
    'if':'ff',
    'fi':'ff',
    'vi':'vf',
    'vf':None,
    }

_logop = {
    'bb': None,
    }

_opmap = {
    'eq': _stdeq,
    'ne': _stdeq,
    'lt': _std,
    'le': _std,
    'gt': _std,
    'ge': _std,
    'add': _stdeq,
    'sub': _stdeq,
    'mul': _vecsca,
    'div': _vecsca,
    'and': _logop,
    'or': _logop,
    'xor': _logop,
    'not': _logop,
    'neg': {
        'i':None,
        'f':None,
        'v':None,
        },
    
    }

class ParamType(object):
    def convert(self, frame, p):
        pass

    def _idx(self, lst, p):
        try:
            idx = lst.index(p)
        except ValueError:
            idx = len(lst)
            lst.append(p)
        return idx

class PNone(ParamType):
    def convert(self, frame, p):
        return 0

    def format(self, p):
        return ""

class PConst(ParamType):
    def format(self, p):
        return repr(p)

class PConstF(PConst):
    def convert(self, frame, p):
        c = frame.consts_f
        return self._idx(c,p)

class PConstI(PConst):
    def convert(self, frame, p):
        c = frame.consts_i
        return self._idx(c,p)

class PConstV(PConst):
    def convert(self, frame, p):
        c = frame.consts_v
        return self._idx(c,p)

class PConstP(PConst):
    def convert(self, frame, p):
        c = frame.consts_p
        return self._idx(c,p)

class PMethod(ParamType):
    def convert(self, frame, p):
        typ,met,ol = p
        for idx,(name,args,rt) in enumerate(typ.method_list):
            if name == met:
                if ol == 0:
                    return idx
                else:
                    ol -= 1
        raise ValueError("invalid method: %s.%s" % p)

    def format(self, p):
        return "%s.%s(%i)" % p

class PProperty(ParamType):
    def convert(self, frame, p):
        typ,met = p
        for idx,(name,rt) in enumerate(typ.prop_list):
            if name == met:
                return idx
        raise ValueError("invalid property: %s.%s" % p)

    def format(self, p):
        return "%s.%s" % p

class PVar(ParamType):
    def format(self, p):
        return p

class PVarI(PVar):
    def convert(self, frame, p):
        c = frame.vars_i
        return self._idx(c,p)

class PVarF(PVar):
    def convert(self, frame, p):
        c = frame.vars_f
        return self._idx(c,p)

class PVarV(PVar):
    def convert(self, frame, p):
        c = frame.vars_v
        return self._idx(c,p)

class PVarP(PVar):
    def convert(self, frame, p):
        c = frame.vars_p
        return self._idx(c,p)

class PNum(ParamType):
    def convert(self, frame, p):
        assert type(p) is int
        return p

    def format(self, p):
        return p
        
_opcodes = [
    ("exit", PNone),
    ("vmcall", PNum),
    
    ("constf", PConstF),
    ("consti", PConstI),
    ("constv", PConstV),
    ("constp", PConstP),

    ("pushvarf", PVarF),
    ("pushvari", PVarI),
    ("pushvarv", PVarV),
    ("pushvarp", PVarP),
    
    ("pop", PNum),

    ("setvarf", PVarF),
    ("setvari", PVarI),
    ("setvarv", PVarV),
    ("setvarp", PVarP),

    ("getprop", PProperty),
    ("setprop", PProperty),
    ("metcall", PMethod),

    ("getpropv", PProperty),
    ("setpropv", PProperty),
    ("metcallv", PMethod),

    ("jump", PNum),
    ("ifjump", PNum),
    
    ("initfor", PVarI),
    ("loop", PNum),

    ("i2f", PNone),
    ("f2i", PNone),
    ("vec2p", PNone),
    ("p2vec", PNone),
    ("lastvec", PNone),
    ]

def _addops():
    addenum = {}
    for op,v in _opmap.iteritems():
        for pf1,pf2 in v.items():
            opcode = "op_"+op+(pf2 or pf1)
            addenum[opcode] = PNone
    addenum = addenum.items()
    addenum.sort()
    _opcodes.extend(addenum)

_addops()

_opcodemap = {}

def _buildmap():
    for idx,(op,param) in enumerate(_opcodes):
        _opcodemap[op] = (idx,param)

_buildmap()

