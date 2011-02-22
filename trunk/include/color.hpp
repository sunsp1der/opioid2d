/*
 * Opioid2D - color
 * Copyright (c) 2006 Sami Hangaslammi <shang@iki.fi>
 * 
 * Utility struct for storing and manipulating color values.
 */
#ifndef OPICOLOR_HPP
#define OPICOLOR_HPP

#include "util.hpp"

#ifdef DARWIN
#include <gl.h>
#else
#include <GL/gl.h>
#endif

namespace opi2d
{   
    struct Color
    {
        float red, green, blue, alpha;
        
        inline Color(float red=1.0, float green=1.0, float blue=1.0, float alpha=1.0)
        {
            this->set(red,green,blue,alpha);
        }
        
        inline Color(const Color& oth)
        {
             *this = oth;
        }
        
        inline void set(float red=1.0, float green=1.0, float blue=1.0, float alpha=1.0)
        {
            this->red = red;
            this->green = green;
            this->blue = blue;
            this->alpha = alpha;
        }
        
        inline void set(const Color& other)
        {
            this->red = other.red;
            this->green = other.green;
            this->blue = other.blue;
            this->alpha = other.alpha;
        }
        
        inline void add(float red=0.0, float green=0.0, float blue=0.0, float alpha=0.0)
        {
            this->red += red;
            this->green += green;
            this->blue += blue;
            this->alpha += alpha;
        }
        
        inline void trimvalues()
        {
            if (this->red < 0) this->red = 0;
            if (this->red > 1) this->red = 1;

            if (this->green < 0) this->green = 0;
            if (this->green > 1) this->green = 1;

            if (this->blue < 0) this->blue = 0;
            if (this->blue > 1) this->blue = 1;

            if (this->alpha < 0) this->alpha = 0;
            if (this->alpha > 1) this->alpha = 1;
        }
        
        inline Color& operator=(const Color& oth)
        {
            
            this->set(oth.red, oth.green, oth.blue, oth.alpha);
            return *this;
        }
        
        inline Color operator*(const Color& oth) const
        {
             return Color(red*oth.red,green*oth.green,blue*oth.blue,alpha*oth.alpha);
        }
        
        inline Color& operator*=(const Color& oth)
        {
            this->red *= oth.red;
            this->green *= oth.green;
            this->blue *= oth.blue;
            this->alpha *= oth.alpha;
            return *this;
        }
        
        inline Color operator*(float mult) const
        {
            return Color(red*mult, green*mult, blue*mult, alpha*mult);
        }
        
        inline Color& operator*=(float mult)
        {
            this->red *= mult;
            this->green *= mult;
            this->blue *= mult;
            this->alpha *= mult;
            return *this;
        }

        inline Color operator/(float d) const
        {
            return Color(red/d, green/d, blue/d, alpha/d);
        }

        
        inline Color operator+(const Color& oth) const
        {
            return Color(red+oth.red, green+oth.green, blue+oth.blue, alpha+oth.alpha);
        }

        inline Color operator-(const Color& oth) const
        {
            return Color(red-oth.red, green-oth.green, blue-oth.blue, alpha-oth.alpha);
        }
        
        inline Color& operator+=(const Color& oth)
        {
            this->add(oth.red, oth.green, oth.blue, oth.alpha);
            return *this;
        }
        
        inline void Apply() const
        {
            glColor4f(red,green,blue,alpha);
        }
    };
}

#endif

