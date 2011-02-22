
#include "opivm.hpp"
#include "opivm_opcodes.hpp"
#include "util.hpp"
#include "vec.hpp"

#include <iostream>
#include <cstring>

namespace opi2d
{
	ExecFrame::ExecFrame(const CodeObj* code)
	{
		this->code = code;
		this->prev = 0;
		this->vararray_f = new floatval[code->varcount_f];
		this->vararray_i = new int[code->varcount_i];
		this->vararray_v = new Vec2[code->varcount_v];
		this->vararray_p = new void*[code->varcount_p];
		this->stack = new unsigned char[code->max_stack];
	}

	ExecFrame::~ExecFrame()
	{
		delete this->vararray_f;
		delete this->vararray_i;
		delete this->vararray_v;
		delete this->vararray_p;
		delete this->stack;
	}
		
	void ExecFrame::restart()
	{
		this->iptr = 0;
		this->prev = 0;
		this->top = this->stack;
		this->vecidx = 0;		
	}
	
	void ExecFrame::execute()
	{
		execute_ops(-1);
		/*while(true)
		{	
			char op = code->code[iptr++];
			char param = code->code[iptr++];
			//std::cout << (int)op << ':' << (int)param << std::endl;
			//std::cout << (int)(top-stack) << std::endl;
			if (op == OPC_EXIT) return;
			execute_op(op,param);
		}*/
	}
	
	void ExecFrame::move(int num, ExecFrame* dst)
	{
		top -= num;
		dst->pushbytes(num, top);
	}

	void ExecFrame::pushbytes(int num, unsigned char* src)
	{
		memcpy(top, src, num);
		top += num;
	}
	
	void ExecFrame::pushv(const Vec2& v)
	{
        /*Vec2* ptr = new Vec2(v);
        cleanup.push_back(ptr);
        pushp(ptr);*/
        pushf(v.x);
        pushf(v.y);
	}
	
}
