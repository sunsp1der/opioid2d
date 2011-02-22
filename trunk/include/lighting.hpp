/*
 * Opioid2D - lighting
 * Copyright (c) 2006 Sami Hangaslammi <shang@iki.fi>
 * 
 * Defines the class for a single light source. The actual rendering
 * logic for lighting is implemented in Scene::CalculateLight and
 * Sprite::Enter. 
 * 
 */
#ifndef OPILIGHT
#define OPILIGHT

#include "util.hpp"

#include "color.hpp"
#include "num.hpp"
#include "vec.hpp"
#include "identified.hpp"

#ifndef NULL
#define NULL 0
#endif

namespace opi2d
{
    class DLLEXPORT Light : public Identified
    {
        public:
        Light() : intensity(0), cutoff(100), node(NULL), pos_update_tick(-1) {}
        
        Color color;
        floatval intensity;
        floatval cutoff;
        
        Vec2 pos;
        Node* node;
        
        Vec2 worldpos;
        int pos_update_tick;
        
    };
}

#endif

