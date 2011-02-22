
#include "opivm.hpp"
#include "vec.hpp"

namespace opi2d
{
	CodeObj::CodeObj()
	{
		conarray_f = 0;
		conarray_i = 0;
		conarray_v = 0;
		conarray_p = 0;
	}
	
	CodeObj::~CodeObj()
	{
		delete conarray_f;
		delete conarray_i;
		delete conarray_v;
		delete conarray_p;
	}
	
	void CodeObj::init_code(const char* code)
	{
		this->code = (const unsigned char*)code; 
	}
	
	void CodeObj::init_const_f(int num)
	{
		this->concount_f = num;
		if (num > 0)
			this->conarray_f = new floatval[num];
	}
	
	void CodeObj::init_const_i(int num)
	{
		this->concount_i = num;
		if (num > 0)
			this->conarray_i = new int[num];		
	}
	
	void CodeObj::init_const_v(int num)
	{
		this->concount_v = num;
		if (num > 0)
			this->conarray_v = new Vec2[num];
	}

	void CodeObj::init_const_p(int num)
	{
		this->concount_p = num;
		if (num > 0)
			this->conarray_p = new void*[num];
	}


	void CodeObj::set_const_f(int idx, floatval f)
	{
		this->conarray_f[idx] = f;
	}
	
	void CodeObj::set_const_i(int idx, int i)
	{
		this->conarray_i[idx] = i;
	}
	
	void CodeObj::set_const_v(int idx, const Vec2& v)
	{
		this->conarray_v[idx] = v;
	}

	void CodeObj::set_const_p(int idx, void* ptr)
	{
		this->conarray_p[idx] = ptr;
	}
	
	
}
