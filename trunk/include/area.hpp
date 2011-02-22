/*
 * Opioid2D - area
 * Copyright (c) 2006 Sami Hangaslammi <shang@iki.fi>
 * 
 * This module implements an area abstraction that is used in e.g. sprite
 * group mutators to test wether a sprite is within a specified area.
 * 
 */
#ifndef OPIAREA
#define OPIAREA

#include "util.hpp"
#include "num.hpp"
#include "vec.hpp"
#include "mat.hpp"

namespace opi2d
{
	/*
	 * The only common functionality for areas (for now) is to check wether
	 * a point belong in the area.  
	 */
	struct Area
	{
		virtual bool contains(const Vec2& p) const = 0;
	};
	
	/*
	 * Rectangular area
	 */
    struct RectArea : public Area
    {
        floatval x,y,xx,yy;
        
        inline RectArea(floatval x,floatval y,floatval xx,floatval yy)
        {
            this->set(x,y,xx,yy);
        }
        
        inline void set(floatval x,floatval y,floatval xx,floatval yy)
        {
            this->x = min(x,xx);
            this->y = min(y,yy);
            this->xx = max(x,xx);
            this->yy = max(y,yy);            
        }
            
        inline bool contains(const Vec2 &p) const
        {
            return (p.x >= x && p.y >= y && p.x <= xx && p.y <= yy);
        }
    };
    
    /*
     * Circular area
     */
    struct CircleArea : public Area
    {
    	floatval x, y, radius;
    	
    	CircleArea(floatval x, floatval y, floatval radius) : x(x), y(y), radius(radius) {}
    	
    	inline bool contains(const Vec2 &p) const
    	{
    		floatval dx = (p.x-x);
    		floatval dy = (p.y-y);
    		if (dx*dx+dy*dy < radius*radius) return true;
    		return false;
    	}
    };
    
    /*
     * Arc, or "pie" shaped area.
     */
    struct ArcArea : public Area
    {
    	floatval x, y, radius, direction, arc;
    	
    	ArcArea(floatval x, floatval y, floatval radius, floatval direction, floatval arc)
    	: x(x), y(y), radius(radius), direction(direction), arc(arc)
    	{    		    		
    	}
    	
    	inline bool contains(const Vec2 &p)
    	{
    		floatval dx = (p.x-x);
    		floatval dy = (p.y-y);
    		if (dx*dx+dy*dy >= radius*radius) return false;
    		Vec2 d(p);
    		d.add(-x,-y);
    		if (angledelta(d.direction(), direction) < arc) return true;
    		return false; 
    	}
    };
}

#endif

