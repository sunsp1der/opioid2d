
#ifndef OPIPATTERN
#define OPIPATTERN

#include "texture.hpp"
#include "vec.hpp"

namespace opi2d
{
	class Pattern : public Texture
	{
	public:
		Pattern(int xsize, int ysize, bool useFilter, int hmode, int vmode);
		
	protected:
	};
}

#endif
