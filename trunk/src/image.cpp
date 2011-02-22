
#include "image.hpp"
#include "debug.hpp"

namespace opi2d
{
    Image::Image(const Texture& tex, int w, int h, float tx, float ty, float txx, float tyy)
    {FUNC
        this->texid = tex.GetTexID();
        this->w = w;
        this->h = h;
        this->tx = tx;
        this->ty = ty;
        this->txx = txx;
        this->tyy = tyy;
        this->hotspot.set(0.5,0.5);
    }
    
    Image::Image()
    {
        this->hotspot.set(0.5,0.5);
    }
    
    Image::~Image()
    {FUNC
    }
    
    void Image::AddCollisionNode(floatval x, floatval y, floatval width, floatval height)
    {
        nodes.push_back(CollisionNode(x,y,width,height));    	
    }
    void Image::ClearCollisionNodes()
    {
    	nodes.clear();
    }
    
    GridImage::GridImage(int cols, int rows) : Image()
    {FUNC
        this->rows = rows;
        this->cols = cols;
        this->images = new Image*[rows*cols];
        this->index = 0;
    }
    
    GridImage::~GridImage()
    {FUNC
        delete this->images;
    }
    
    void GridImage::AppendImage(Image* image)
    {FUNC
        this->images[this->index++] = image;
    }
    
    void GridImage::SetSize(int w, int h)
    {FUNC
        this->w = w;
        this->h = h;
    }
}

