/*
 * Opioid2D - display
 * Copyright (c) 2006 Sami Hangaslammi <shang@iki.fi>
 * 
 *  
 */

#ifndef OPIDISPLAY_HPP
#define OPIDISPLAY_HPP

#include "vec.hpp"
#include "color.hpp"
#include "singleton.hpp"

namespace opi2d
{
    class Display : public Singleton<Display>
    {
    public:      
        void Clear();
        void SetClearColor(const Color& color);
        
        // If this flag is set to false, then all calls to Display::Clear are ignored. 
        void EnableClearing(bool flag);
        
        void InitView(int xres, int yres, int xunits, int yunits);
    
        inline const Vec2& GetViewSize() { return this->units; }
        
    protected:
        friend class Singleton<Display>;
        Display();
        
        Color _clearColor;
        bool clearing;
        
        Vec2 res;
        Vec2 units;
    };
}

#endif

