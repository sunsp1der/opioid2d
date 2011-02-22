
#ifndef VEC_HPP
#define VEC_HPP

#include <cmath>

#include "num.hpp"
#include "util.hpp"

namespace opi2d
{
	class ExecFrame;
	
    class Vec2
    {
        public:
        floatval x,y;
        
        // Constructors
        
        inline Vec2() : x(0),y(0) 
        {
        }
        
        inline Vec2(floatval xval, floatval yval) : x(xval),y(yval)
        {
        }
        
        inline Vec2(const Vec2& other) : x(other.x), y(other.y)
        {
        }
        
        // Operators
        inline Vec2& set(floatval x, floatval y)
        {
            this->x = x;
            this->y = y;
            return *this;
        }
        
        inline Vec2& set(const Vec2& other)
        {
            this->x = other.x;
            this->y = other.y;
            return *this;
        }
        
        inline Vec2& operator=(const Vec2& other)
        {
            this->x = other.x;
            this->y = other.y;
            return *this;
        }
        
        inline Vec2 operator-() const
        {
        	return Vec2(-x,-y);
        }        
        
        inline bool cmp(const Vec2& other) const
        {
            return (this->x == other.x) && (this->y == other.y);
        }
        
        inline bool cmp(floatval x, floatval y) const
        {
            return (this->x == x) && (this->y == y);
        }
        
        inline Vec2& add(floatval dx, floatval dy)
        {
            this->x += dx;
            this->y += dy;
            return *this;
        }
        inline Vec2& add(const Vec2& oth)
        {
            this->x += oth.x;
            this->y += oth.y;
            return *this;
        }
        inline Vec2& sub(floatval dx, floatval dy)
        {
            this->x -= dx;
            this->y -= dy;
            return *this;
        }
        inline Vec2& sub(const Vec2& oth)
        {
            this->x -= oth.x;
            this->y -= oth.y;
            return *this;
        }

        inline Vec2& mul(floatval m)
        {
            this->x *= m;
            this->y *= m;
            return *this;
        }
        inline Vec2& mul(floatval mx, floatval my)
        {
            this->x *= mx;
            this->y *= my;
            return *this;
        }
        inline Vec2& mul(const Vec2& oth)
        {	
            this->x *= oth.x;
            this->y *= oth.y;
            return *this;
        }
        inline Vec2& div(floatval d)
        {
        	this->x /= d;
        	this->y /= d;
        	return *this;
        }
        inline Vec2& div(floatval dx, floatval dy)
        {
        	this->x /= dx;
        	this->y /= dy;
        	return *this;
        }
        inline Vec2& div(const Vec2& oth)
        {
        	this->x /= oth.x;
        	this->y /= oth.y;
        	return *this;
        }
        inline void xyabs()
        {
        	this->x = fabs(this->x);
        	this->y = fabs(this->y); 
        }
        
        inline Vec2& operator+=(const Vec2& other)
        {
            this->add(other);
            return *this;
        }
        inline Vec2& operator-=(const Vec2& other)
        {
            this->add(-other.x,-other.y);
            return *this;
        }
        inline Vec2& operator*=(const Vec2& other)
        {
            this->mul(other);
            return *this;
        }
        inline Vec2& operator*=(floatval mul)
        {
            this->mul(mul);
            return *this;
        }
        
        
        
        inline Vec2 operator+(const Vec2& other) const
        {
            return Vec2(this->x+other.x,this->y+other.y);
        }
        inline Vec2 operator-(const Vec2& other) const
        {
            return Vec2(this->x-other.x,this->y-other.y);
        }
        inline Vec2 operator*(floatval mul) const
        {
            return Vec2(this->x*mul,this->y*mul);
        }
        inline Vec2 operator/(floatval div) const
        {
        	return Vec2(this->x/div, this->y/div);
        }
        
        inline Vec2 dot(const Vec2& other) const
        {
            return Vec2(this->x*other.x, this->y*other.y);
        }
        
        
        inline Vec2 rad2xy() const
        {
            float angle = x * DEG2RAD + PI;
            return Vec2(-sin(angle) * y, cos(angle)*y);
        }
        
        inline Vec2 xy2rad() const
        {
            return Vec2(this->direction(), this->length());
        }
        
        inline void set_radial(floatval dir, floatval len)
        {
            float angle = dir * DEG2RAD + PI;
            set(-sin(angle) * len, cos(angle)*len);        	
        }
        
        inline floatval length() const
        {
            return sqrt(x*x+y*y);
        }
        
        inline void set_length(floatval l)
        {
        	floatval d = this->direction();
        	set_radial(d, l);
        }
        
        inline Vec2 unitvec() const
        {
            floatval l = this->length();
            if (l == 0)
            {
            	return Vec2(0, -1);
            }
            return Vec2(x/l,y/l);
        }
        
        inline Vec2 ortho() const
        {
            return Vec2(y,-x);
        }
        
        inline Vec2 orthounit() const
        {
            floatval l = this->length();
            if (l == 0)
            {
            	return Vec2(0, -1);
            }
            return Vec2(y/l,-x/l);
        }
        
        inline floatval direction() const
        {
            floatval l = this->length();
            if (l == 0) return 0;
            floatval dot = -y/l;
            floatval angle = -acos(dot) / PI * 180.0;
            if (x > 0) angle = 360-angle;
            return angle;
        }
        
        inline void set_direction(floatval d)
        {
        	floatval l = length();
        	set_radial(d, l);
        }
        
        inline floatval angle(const Vec2& other)
        {
            return other.direction() - this->direction();
        }
        
        void VM_GetProp(ExecFrame* f, int idx);
		void VM_SetProp(ExecFrame* f, int idx);
		void VM_MetCall(ExecFrame* f, int idx);       
         
    };
    
    struct Rect
    {
    	Vec2 topleft;
    	Vec2 size;
    	
    	inline Rect() {}
    	inline Rect(floatval x, floatval y, floatval w, floatval h) : topleft(x,y), size(w,h) {}
    	inline Rect(const Rect& r) : topleft(r.topleft), size(r.size) {}
    	
    	inline bool contains(const Vec2& p)
    	{
    		return (p.x >= topleft.x && p.y >= topleft.y && p.x < topleft.x+size.x && p.y < topleft.y+size.y);
    	}
    };
    
    struct FreeRect
    {
    	Vec2 points[4];

		FreeRect() {}
		FreeRect(const Rect& src)
		{
			floatval x = src.topleft.x;
			floatval y = src.topleft.y;
			floatval xx = x + src.size.x;
			floatval yy = y + src.size.y;
			points[0] = src.topleft;
			points[1].set(xx,y);
			points[2].set(xx,yy);
			points[3].set(x,yy); 
		}
    	   	
    	inline bool contains(const Vec2& p) const
    	{
    		// adapted from http://local.wasp.uwa.edu.au/~pbourke/geometry/insidepoly/
    		// Copyright (c) Paul Bourke
    		// TODO: need to check license
    		int counter = 0;
    		Vec2 p1, p2;
    		floatval xinters;
    		const int N=4;
    		p1 = points[0];
    		for(int i=1; i<=N; ++i)
    		{
    			p2 = points[i % N];
    			if (p.y > min(p1.y, p2.y))
    			{
    				if (p.y <= max(p1.y, p2.y))
    				{
    					if (p.x <= max(p1.x, p2.x))
    					{
    						if (p1.y != p2.y)
    						{
    							xinters = (p.y-p1.y)*(p2.x-p1.x)/(p2.y-p1.y)+p1.x;
    							if (p1.x == p2.x || p.x <= xinters)
    							{
    								++counter;
    							}
    						}
    					}
    				}
    			}
    			p1 = p2;
    		}
    		return (counter % 2 != 0);
    	}
    };
    
}


#endif

