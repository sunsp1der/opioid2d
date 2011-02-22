
#ifndef OPIVM_INTERFACE
#define OPIVM_INTERFACE

#include "opivm.hpp"

namespace opi2d
{
	class VMInterface
	{
		public:
		virtual void VM_SetProp(ExecFrame* f, int idx) = 0;
		virtual void VM_GetProp(ExecFrame* f, int idx) = 0;
		virtual void VM_MetCall(ExecFrame* f, int idx) = 0;
	};
}

#endif

