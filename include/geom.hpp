
#ifndef OPIGEOM_HPP
#define OPIGEOM_HPP

#include <vector>
#include "num.hpp"
#include "vec.hpp"

namespace opi2d
{
	typedef std::vector<Vec2> GeomPoints;
	
	class GeomPrimitive
	{
	public:
		
		virtual void draw() const = 0;
		virtual void draw_aa() const;
		
	protected:
	};
	
	class GeomLine : public GeomPrimitive
	{
	public:
		GeomLine(floatval x, floatval y, floatval xx, floatval yy);
		void draw() const;
		void draw_aa() const;
	protected:
		floatval x,y,xx,yy;
	};
	
	class GeomLines : public GeomPrimitive
	{
	};
	
}

#endif
