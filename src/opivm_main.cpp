
#include "opivm.hpp"
#include "num.hpp"

namespace opi2d
{
	int get_int_size()
	{
		return sizeof(int);
	}
	
	int get_float_size()
	{
		return sizeof(floatval);
	}
	
	int get_ptr_size()
	{
		return sizeof(void*);
	}

}
