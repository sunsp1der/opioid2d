/*
#ifdef DARWIN
#include <SDL.h>
#else
#include <SDL/SDL.h>
#endif
*/
#include "opioid2d.hpp"
#include "rendering.hpp"
#include "debug.hpp"

namespace opi2d
{
    void InitOpioid2D()
    {
        DEBUG("InitOpioid2D");
        Display::Init();
        Director::Init();
        RenderingEngine::Init();
        SpriteMapper::Init();
    }
    
    void QuitOpioid2D()
    {
        DEBUG("QuitOpioid2D");
        SpriteMapper::Destroy();
        Director::Destroy();
        Display::Destroy();
        RenderingEngine::Destroy();
        DEBUG("SDL_Quit succesful");
    }
}

