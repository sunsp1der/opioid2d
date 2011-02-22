
#include "util.hpp"

#ifdef DARWIN
#include <gl.h>
#else
#include <GL/gl.h>
#endif

#include <cstdlib>
#include <iostream>
#include "rendering.hpp"
#include "num.hpp"
#include "debug.hpp"

namespace opi2d
{
    void RenderingQueue::IncreaseCapacity()
    {FUNC
        this->capacity = (int)(this->capacity*1.2+50);
        vertex_array = (quad_vertices*)realloc(vertex_array, sizeof(quad_vertices)*capacity);
        texco_array = (quad_vertices*)realloc(texco_array, sizeof(quad_vertices)*capacity);
        color_array = (quad_colors*)realloc(color_array, sizeof(quad_colors)*capacity);
    }

    RenderingQueue::RenderingQueue(int capacity)
    {FUNC
        DEBUG("Creating a rendering queue");
        vertex_array = (quad_vertices*)malloc(sizeof(quad_vertices)*capacity);
        texco_array = (quad_vertices*)malloc(sizeof(quad_vertices)*capacity);
        color_array = (quad_colors*)malloc(sizeof(quad_colors)*capacity);
        this->capacity = capacity;
        numQuads = 0;
    }
    RenderingQueue::~RenderingQueue()
    {FUNC
        free(vertex_array);
        free(texco_array);
        free(color_array);
    }
   
    void RenderingQueue::Clear()
    {//FUNC
        numQuads = 0;
    }
    
    void RenderingQueue::Render()
    {//FUNC
        #ifdef USE_FLOATS
        glVertexPointer(2, GL_FLOAT, 0, this->vertex_array);
        glTexCoordPointer(2, GL_FLOAT, 0, this->texco_array);
        glColorPointer(4, GL_FLOAT, 0, this->color_array);
        #else
        glVertexPointer(2, GL_DOUBLE, 0, this->vertex_array);
        glTexCoordPointer(2, GL_DOUBLE, 0, this->texco_array);
        glColorPointer(4, GL_FLOAT, 0, this->color_array);
        #endif
        if (glGetError() != GL_NO_ERROR)
        {
            DEBUG("ERROR in setting array pointers");
        }
        //DEBUG("glDrawArrays");
        glDrawArrays(GL_QUADS, 0, this->numQuads*4);
        if (glGetError() != GL_NO_ERROR)
        {
            DEBUG("ERROR in glDrawArrays");
        }
        //DEBUG("RenderingQueue::Render completed");
    }
    
    RenderingEngine::~RenderingEngine()
    {FUNC
        this->Clear();
    }
    
    void RenderingEngine::Clear()
    {//FUNC
        for(QueueMap::iterator i=queues.begin();i!=queues.end();++i)
        {
            delete i->second;
        }
        this->queues.clear();
        //DEBUG("RenderingEngine cleared");
    }
    
    void RenderingEngine::EmptyQueues()
    {//FUNC
        for(QueueMap::iterator i=queues.begin();i!=queues.end();++i)
        {
            i->second->Clear();
        }
    }
    
    void RenderingEngine::Render()
    {//FUNC
        for(QueueMap::iterator i=queues.begin();i!=queues.end();++i)
        {        	
            int texid = i->first.second;
            //std::cout << "binding texture " << texid << std::endl;
            if (texid == 0)
            {  
                //DEBUG("Rendering with solid color");
                glDisable(GL_TEXTURE_2D);
                i->second->Render();
                glEnable(GL_TEXTURE_2D);
            }
            else
            {
                //DEBUG("Rendering with a texture");
                glBindTexture(GL_TEXTURE_2D, texid);
                i->second->Render();
            }
        }
        //this->EmptyQueues();
    }
}
