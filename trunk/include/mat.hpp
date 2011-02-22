/*
 * Opioid2D - mat
 * Copyright (c) 2006 Sami Hangaslammi <shang@iki.fi>
 * 
 * Utility class for matrix operations.
 */
#ifndef OPIMAT_HPP
#define OPIMAT_HPP

#include <cstring>
#include <cmath>

#include "num.hpp"
#include "vec.hpp"

#ifndef PI
#define PI (3.141592653589793)
#endif

namespace opi2d
{    
    /*
     * A nine-item (3x3) matrix for calculating transformations in 2D.
     */
    class Mat9
    {
        public:
        floatval value[9];
    
        inline Mat9()
        {
        }
        
        inline Mat9(floatval* src)
        {
            memcpy(value, src, sizeof(floatval)*9);
        }

        inline Mat9(const Mat9& other)
        {
            memcpy(value, other.value, sizeof(floatval)*9);
        }

        inline Mat9& operator=(const Mat9& other)
        {
            memcpy(value, other.value, sizeof(floatval)*9);
            return *this;
        }
        
        inline floatval get(int index) const { return value[index]; }
        inline void set(int index, floatval val) { value[index] = val; }
        
        inline void identity()
        {
            const floatval oth[9] = 
            {
              1,0,0,
              0,1,0,
              0,0,1,
            };
            memcpy(value,oth,sizeof(floatval)*9);
        }
        
        inline floatval determinant() const
        {
        	return value[0]*value[4] - value[1]*value[3];        		 
        }
        
        inline Mat9 inversed() const
        {
        	Mat9 result;
        	floatval* i = result.value;
        	floatval d = 1.0/determinant();
        	
        	floatval C1 = value[1]*value[5] - value[2]*value[4];
        	floatval C2 = value[0]*value[5] - value[2]*value[3];
        	
        	i[0] = d * value[4];
        	i[1] = -d * value[1];
        	i[2] = d * C1;
        	
        	i[3] = -d * value[3];
        	i[4] = d * value[0];
        	i[5] = -d * C2;
        	
        	i[6] = 0;
        	i[7] = 0;
        	i[8] = 1;
        	       	
        	return result;
        }
        
        inline void mul(const Mat9& other)
        {
            mul(other.value);
        }

        inline void mul(const floatval* oth)
        {
            floatval org[9];
            memcpy(org, value, sizeof(floatval)*9);
            for(int i=0;i<3;++i)
            for(int k=0;k<3;++k)
            {
                value[i+k*3] = 0;
                for(int j=0;j<3;++j)
                    value[i+k*3] += oth[i+j*3] * org[j+k*3];
            }
        }

        inline void transform(Vec2& vec) const
        {
            floatval x = vec.x;
            floatval y = vec.y;
            vec.x = x*value[0] + y*value[1] + value[2];
            vec.y = x*value[3] + y*value[4] + value[5];
        }
        
        inline void transform(FreeRect& rect) const
        {
        	for(int i=0;i<4;++i)
        	{
        		this->transform(rect.points[i]);
        	}
        }
        
        inline FreeRect transform(const Rect& rect) const
        {
        	FreeRect result(rect);
        	this->transform(result);
        	return result;
        }
     
        inline void translate(floatval x, floatval y)
        {
            const floatval oth[9] = 
            {
              1,0,x,
              0,1,y,
              0,0,1
            };
            mul(oth);
        }
     
        inline void translate(const Vec2& delta)
        {
            translate(delta.x,delta.y);
        }
        
        inline void scale(floatval x, floatval y)
        {
            const floatval oth[9] =
            {
              x,0,0,
              0,y,0,
              0,0,1,
            };
            mul(oth);
        }
      
        inline void scale(const Vec2& s)
        {
            scale(s.x,s.y);
        }

        inline void rotate(floatval angle)
        {
            angle *= -PI/180.0;
            const floatval oth[9] = 
            {
                cos(angle), sin(angle), 0,
                -sin(angle), cos(angle), 0,
                0, 0, 1
            };
            mul(oth);
        }
    
    };
   
}


#endif

