/*
 * Opioid2D - image
 * Copyright (c) 2006 Sami Hangaslammi <shang@iki.fi>
 * 
 * Defines the structure for a single image on a texture page.
 */
#ifndef OPIIMAGE
#define OPIIMAGE

#include "util.hpp"

#include "vec.hpp"
#include "texture.hpp"
#include "collision.hpp"

namespace opi2d
{
    class Image
    {
        public:
        Image(const Texture& tex, int w, int h, float tx, float ty, float txx, float tyy);
        virtual ~Image();
        
        int texid;
        int w,h;
        float tx,ty,txx,tyy;
        
        Vec2 hotspot;
        
        inline virtual bool IsGrid() const { return false; }
        void AddCollisionNode(floatval x, floatval y, floatval width, floatval height);
        void ClearCollisionNodes();
        
        
        protected:
        friend class Scene;
        friend class Sprite;
        CollisionNodes nodes;
        Image();
    };
    
    class GridImage : public Image
    {
        public:
        GridImage(int cols, int rows);
        virtual ~GridImage();
        
        void AppendImage(Image* image);
        void SetSize(int w, int h);
        
        inline virtual bool IsGrid() const { return true; }

        int rows;
        int cols;        
        Image** images;

        protected:
        int index;
    };
}

#endif

