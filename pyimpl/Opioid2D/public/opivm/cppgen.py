
import Opioid2D.public.opivm.opcodes as opcodes

def gen_opcode_header():
    result = []
    app = result.append
    for idx,(op,param) in enumerate(opcodes._opcodes):
        app("#define OPC_%s %i" % (op.upper(), idx))
    return "\n".join(result)

def gen_vmswitch_stub():
    result = []
    app = result.append
    app("switch(opcode) {")
    for idx,(op,param) in enumerate(opcodes._opcodes):
        const = "OPC_%s" % op.upper()
        app("    case %s:" % const)
        app("        ; // TODO")
        app("        break;")
    app("}")
    return "\n".join(result)
        
