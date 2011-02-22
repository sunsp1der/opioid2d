
#ifndef OPIVM
#define OPIVM

#include "num.hpp"
#include "vec.hpp"

namespace opi2d
{
	extern int get_int_size();
	extern int get_float_size();
	extern int get_ptr_size();
	
	struct CodeObj
	{
		CodeObj();
		~CodeObj();

		const unsigned char* code;
		
		int concount_f;
		int concount_i;
		int concount_v;
		int concount_p;
		
		floatval* conarray_f;
		int* 	  conarray_i;
		Vec2* 	  conarray_v;
		void** 	  conarray_p;
		
		int varcount_f;
		int varcount_i;
		int varcount_v;
		int varcount_p;

		int max_stack;
		
		void init_code(const char* code);
		
		void init_const_f(int num);
		void init_const_i(int num);
		void init_const_v(int num);
		void init_const_p(int num);

		void set_const_f(int idx, floatval f);
		void set_const_i(int idx, int i);
		void set_const_v(int idx, const Vec2& v);
		void set_const_p(int idx, void* ptr);
	};

	class Sprite;

	struct ExecFrame
	{
		ExecFrame(const CodeObj* code);
		ExecFrame(const CodeObj* code, ExecFrame* prev);
		~ExecFrame();
				
		const CodeObj* code;

		unsigned char* stack;
		unsigned char* top;
		int iptr;		

		float* vararray_f;
		int*   vararray_i;
		Vec2*  vararray_v;
		void** vararray_p;
		
		Vec2   vectemp[5];
		int    vecidx;
		
		ExecFrame* prev;
		
		void restart();
		
		void execute();
		void execute_ops(int num);
		
		void move(int num, ExecFrame* dst);
		
		void pushbytes(int num, unsigned char* src);
		
		inline Sprite* popSprite()
		{
			return (Sprite*)popp();
		}
		
		inline void pushf(floatval f)
		{
	        *((floatval*)(top)) = f;
	        top += sizeof(floatval);			
		}
		inline void pushi(int i)
		{
	        *((int*)(top)) = i;
	        top += sizeof(int);			
		}

		void pushv(const Vec2& v);

		inline void pushp(void* ptr)
		{
	        *((void**)(top)) = ptr;
	        top += sizeof(void*);
		}
		
		inline floatval popf()
		{
			top -= sizeof(floatval);
			return *((floatval*)top);
		}
		inline int popi()
		{
			top -= sizeof(int);
			return *((int*)top);
		}
		inline void* popp()
		{
			top -= sizeof(void*);
			return *((void**)top);
		}
		inline Vec2* popv()
		{
			return (Vec2*)popp();
		}
	};

	

}

#endif

