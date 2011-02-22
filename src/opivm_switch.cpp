
#include "util.hpp"

#include <cstdlib>
#include <iostream>

#include "opivm.hpp"
#include "opivm_interface.hpp"
#include "opivm_opcodes.hpp"
#include "vec.hpp"


namespace opi2d
{
	void ExecFrame::execute_ops(int num)
	{
		int opcode, param;
		floatval fa,fb;
		int ia, ib, ifor, iparam, ijmp;
		//char opfor,pfor;
		Vec2 *v1,*v2;
		Vec2 v;
		VMInterface* obj;
		ExecFrame* frame;
		CodeObj* cobj;
		
		while(num-- != 0)
		{
			opcode = (int)code->code[iptr++];
			param = (int)code->code[iptr++];
			
			//std::cout << opcode << ':' << param << std::endl;
			
			switch(opcode) {
				case OPC_EXIT:
					iptr-=2;
					return;
				case OPC_VMCALL:
					cobj = (CodeObj*)popp();
					ia = popi();
					frame = new ExecFrame(cobj);
					frame->restart();
					if (param > 0) move(param, frame);
					frame->execute();
					if (ia > 0) frame->move(ia, this);
					delete frame;
					break;
			    case OPC_CONSTF:
			    	pushf(code->conarray_f[param]);
			        break;
			    case OPC_CONSTI:
			        pushi(code->conarray_i[param]);
			        break;
			    case OPC_CONSTV:
			    	pushv(code->conarray_v[param]);
			        break;
			    case OPC_CONSTP:
			    	pushp(code->conarray_p[param]);
			    	break;
			    case OPC_PUSHVARF:
			        pushf(vararray_f[param]);
			        break;
			    case OPC_PUSHVARI:
			        pushi(vararray_i[param]);
			        break;
			    case OPC_PUSHVARV:
			        pushv(vararray_v[param]);
			        break;
			    case OPC_PUSHVARP:
			        pushp(vararray_p[param]);
			        break;
				case OPC_POP:
					top -= param;
					break;
			    case OPC_SETVARF:
			        vararray_f[param] = popf();
			        break;
			    case OPC_SETVARI:
			        vararray_i[param] = popi();
			        break;
			    case OPC_SETVARV:
			    	fb = popf();
			    	fa = popf();
			        vararray_v[param].set(fa,fb);
			        break;
			    case OPC_SETVARP:
			        vararray_p[param] = popp();
			        break;
			    case OPC_GETPROP:
			        obj = (VMInterface*)popp();
			        obj->VM_GetProp(this, param);
			        break;
			    case OPC_SETPROP:
			        obj = (VMInterface*)popp();
			        obj->VM_SetProp(this, param);
			        break;
			    case OPC_METCALL:
			        obj = (VMInterface*)popp();
			        obj->VM_MetCall(this, param);
			        break;
			    case OPC_GETPROPV:
			        v1 = (Vec2*)popp();
			        v1->VM_GetProp(this, param);
			        break;
			    case OPC_SETPROPV:		    
			        v1 = (Vec2*)popp();
			        v1->VM_SetProp(this, param);
			        break;
			    case OPC_METCALLV:
			        v1 = (Vec2*)popp();
			        v1->VM_MetCall(this, param);
			        break;
			    case OPC_JUMP:
			        iptr += param*2;
			        break;
			    case OPC_IFJUMP:
			        ia = popi();
			        if (ia == 0) iptr += param*2;
			        break;
			    case OPC_INITFOR:
			        ib = popi();
			        ia = popi();
			        ++iptr;
			        iparam = code->code[iptr++];
			        ijmp = iptr;
			        for(ifor=ia;ifor<ib;++ifor)
			        {
			        	iptr = ijmp;
			        	vararray_i[param] = ifor;
			        	execute_ops(iparam);
			        	/*for(iptr=ijmp;iptr<ijmp+iparam*2;++iptr)
			        	{
					        opfor = code->code[iptr];
					        pfor = code->code[++iptr];
					        if (opfor == OPC_EXIT)
					        {
					        	--iptr;
					        	return;
					        }
			        		execute_op(opfor, pfor);
			        	}*/
			        	 
			        }
			        break;
			    case OPC_LOOP:
			        ; // TODO
			        break;
			    case OPC_I2F:
			    //  this will break is floatval uses doubles !!
			    /*    ia = *((int*)top);
			        *((floatval*)top) = (float)ia;*/
			        ia = popi();
			        pushf((floatval)ia);		        
			        break;
			    case OPC_F2I:
			        /*fa = *((floatval*)top);
			        *((int*)top) = (int)fa;*/
			        fa = popf();
			        pushi((int)fa);		        
			        break;
			    case OPC_VEC2P:
			    	fb = popf();
			    	fa = popf();
			    	v1 = vectemp + (vecidx % 5);
			    	++vecidx;
			    	v1->set(fa,fb);
			    	pushp(v1);
			    	break;
			    case OPC_P2VEC:
			    	v1 = popv();
			    	pushv(*v1);
			    	break;
			    case OPC_LASTVEC:
			    	v1 = vectemp + ((vecidx-1)%5);
			    	pushv(*v1);
			    	break;
			        
		// --------------------------------------------------
		// -------------------- OPERATORS -------------------
		// --------------------------------------------------		        
			        
			    case OPC_OP_ADDFF:
			    	fa = popf();
			        *(((floatval*)top)-1) += fa;
			        break;
			    case OPC_OP_ADDII:
			    	ia = popi();
			        *(((int*)top)-1) += ia;
			        break;
			    case OPC_OP_ADDVV:
			        v2 = popv();
			        v1 = popv();
			        v.set(*v1);
			        v.add(*v2);
			        pushv(v);
			        break;
			    case OPC_OP_ANDBB:
			        ib = popi();
			        ia = popi();
			        pushi(ia & ib);
			        break;
			    case OPC_OP_DIVFF:
			    	fa = popf();
			        *(((floatval*)top)-1) /= fa;
			        break;
			    case OPC_OP_DIVII:
			    	ia = popi();
			        *(((int*)top)-1) /= ia;
			        break;
			    case OPC_OP_DIVVF:
			        fa = popf();
			        v1 = (Vec2*)popp();
			        v.set(*v1);
			        v.div(fa);
			        pushv(v);
			        break;
			    case OPC_OP_EQFF:
			        fb = popf();
			        fa = popf();
			        pushi((int)(fa == fb));
			        break;
			    case OPC_OP_EQII:
			        ib = popi();
			        ia = popi();
			        pushi((int)(ia == ib));
			        break;
			    case OPC_OP_EQVV:
			        v2 = popv();
			        v1 = popv();
			        pushi((int)(ia == ib));
			        break;
			    case OPC_OP_GEFF:
			        fb = popf();
			        fa = popf();
			        pushi((int)(fa >= fb));
			        break;
			    case OPC_OP_GEII:
			        ib = popi();
			        ia = popi();
			        pushi((int)(ia >= ib));
			        break;
			    case OPC_OP_GTFF:
			        fb = popf();
			        fa = popf();
			        pushi((int)(fa > fb));
			        break;
			    case OPC_OP_GTII:
			        ib = popi();
			        ia = popi();
			        pushi((int)(ia > ib));
			        break;
			    case OPC_OP_LEFF:
			        fb = popf();
			        fa = popf();
			        pushi((int)(fa <= fb));
			        break;
			    case OPC_OP_LEII:
			        ib = popi();
			        ia = popi();
			        pushi((int)(ia <= ib));
			        break;
			    case OPC_OP_LTFF:
			        fb = popf();
			        fa = popf();
			        pushi((int)(fa < fb));
			        break;
			    case OPC_OP_LTII:
			        ib = popi();
			        ia = popi();
			        pushi((int)(ia < ib));
			        break;
			    case OPC_OP_MULFF:
			    	fa = popf();
			        *(((floatval*)top)-1) *= fa;
			        break;
			    case OPC_OP_MULII:
			    	ia = popi();
			        *(((int*)top)-1) *= ia;
			        break;
			    case OPC_OP_MULVF:
			        fa = popf();
			        v1 = popv();
			        v.set(*v1);
			        v.mul(fa);
			        pushv(v);
			        break;
			    case OPC_OP_NEFF:
			        fb = popf();
			        fa = popf();
			        pushi((int)(fa != fb));
			        break;
			    case OPC_OP_NEGF:
			        *(((floatval*)top)-1) = -(*((floatval*)top));
			        break;
			    case OPC_OP_NEGI:
			        *(((int*)top)-1) = -(*((int*)top));
			        break;
			    case OPC_OP_NEGV:
			        v1 = popv();
			        v.set(-v1->x, -v1->y);
			        pushv(v);
			        break;
			    case OPC_OP_NEII:
			        ib = popi();
			        ia = popi();
			        pushi((int)(ia != ib));
			        break;
			    case OPC_OP_NEVV:
			        v2 = popv();
			        v1 = popv();
			        pushi((int)(ia != ib));
			        break;
			    case OPC_OP_NOTBB:
			        ; // TODO
			        break;
			    case OPC_OP_ORBB:
			        ; // TODO
			        break;
			    case OPC_OP_SUBFF:
			    	fa = popf();
			        *(((floatval*)top)-1) -= fa;
			        break;
			    case OPC_OP_SUBII:
			    	ia = popi();
			        *(((int*)top)-1) -= ia;
			        break;
			    case OPC_OP_SUBVV:
			        v2 = (Vec2*)popp();
			        v1 = (Vec2*)popp();
			        v.set(*v1);
			        v.sub(*v2);
			        pushv(v);
			        break;
			    case OPC_OP_XORBB:
			        ; // TODO
			        break;
			}
		}
	}
}
