#ifdef O2D_MSVC
#include <windows.h>
#endif

#include "display.hpp"
#include "debug.hpp"

namespace opi2d
{
    void _init_gl()
    {FUNC
        glClearColor(0,0,0,0);
        glDisable(GL_DEPTH_TEST);
        glDisable(GL_ALPHA_TEST);
        glEnable(GL_BLEND);
        glEnable(GL_TEXTURE_2D);
        glShadeModel(GL_SMOOTH);
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
        
        glEnableClientState(GL_VERTEX_ARRAY);
        glEnableClientState(GL_COLOR_ARRAY);
        glEnableClientState(GL_TEXTURE_COORD_ARRAY);
        
        glClear(GL_COLOR_BUFFER_BIT);
        
        if (glGetError() != GL_NO_ERROR)
        {
            DEBUG("ERROR: intializing opengl failed somehow");            
        }
    }
    
    void _init_projection(int xunits, int yunits)
    {FUNC
        glMatrixMode(GL_PROJECTION);
        glLoadIdentity();
        glOrtho(0,xunits, yunits, 0, -1, 1);
        glMatrixMode(GL_MODELVIEW);
        glLoadIdentity();
    }


    Display::Display() : _clearColor(0,0,0,1), clearing(true),
    res(0,0), units(0,0)
    {FUNC
    }
         
    void Display::Clear()
    {FUNC
        if (!this->clearing) return;
        if (this->_clearColor.alpha != 1.0)
        {
            glLoadIdentity();
            this->_clearColor.Apply();
            glDisable(GL_TEXTURE_2D);
            glBegin(GL_QUADS);
            glVertex2f(0,0);
            glVertex2f(units.x,0);
            glVertex2f(units.x,units.y);
            glVertex2f(0,units.y);
            glEnd();
            glEnable(GL_TEXTURE_2D);
        }
        else
        {
            glClear(GL_COLOR_BUFFER_BIT);
        }
    }
    
    void Display::SetClearColor(const Color& color)
    {FUNC
        this->_clearColor = color;
        this->clearing = true;
        glClearColor(color.red, color.green, color.blue, color.alpha);
    }
    
    void Display::EnableClearing(bool flag)
    {
        this->clearing = flag;
    }
                
    void Display::InitView(int xres, int yres, int xunits, int yunits)
    {FUNC
        this->res.set(xres, yres);
        _init_gl();
        this->units.set(xunits, yunits);
        _init_projection(xunits, yunits);
    }
        
}
