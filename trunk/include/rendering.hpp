// utilities for the rendering queue
#ifndef OPIRENDERING_HPP
#define OPIRENDERING_HPP

#include "util.hpp"

#include <cstring>
#include <map>
#include <utility>

#include "num.hpp"
#include "vec.hpp"
#include "color.hpp"
#include "singleton.hpp"
#include "debug.hpp"

namespace opi2d
{
    struct quad_vertices
    {
        Vec2 pts[4];
    };
   
    struct quad_colors
    {
        Color rgba[4];
    };
   

    class RenderingQueue
    {
    public:
        quad_vertices* vertex_array;
        quad_vertices* texco_array;
        quad_colors* color_array;
        int numQuads;
        int capacity;

        RenderingQueue(int capacity=100);
        ~RenderingQueue();
    
        void Render();
        
        inline void AppendQuad(const quad_vertices* va, const quad_vertices* ta, const quad_colors* ca)
        {//FUNC
             if (numQuads == capacity)
            {
                  IncreaseCapacity();
            }
             
             memcpy(vertex_array+numQuads, va, sizeof(quad_vertices));
             memcpy(texco_array+numQuads, ta, sizeof(quad_vertices));
             memcpy(color_array+numQuads, ca, sizeof(quad_colors));
             ++numQuads;
        }
        
        void IncreaseCapacity();
        void Clear();
    };
    
    typedef std::map<std::pair<int,int>, RenderingQueue*> QueueMap;
    
    class RenderingEngine : public Singleton<RenderingEngine>
    {
        public:
        RenderingEngine() : ignoreColor(false) 
        {
            black.rgba[0].set(0,0,0);
            black.rgba[1].set(0,0,0);
            black.rgba[2].set(0,0,0);
            black.rgba[3].set(0,0,0);
        }

        ~RenderingEngine();    
        
        inline void AppendQuad(int zorder, int texid, const quad_vertices* va, const quad_vertices* ta, const quad_colors* ca)
        {//FUNC
            //std::cout << "AppendQuad " << texid << std::endl;
            QueueMap::iterator i = queues.find(std::pair<int,int>(zorder,texid));
            RenderingQueue* queue;
            if (i==queues.end())
            {
                queue = new RenderingQueue();
                queues[std::pair<int,int>(zorder,texid)] = queue;
            }
            else
            {
                queue = i->second;
            }
            if (ignoreColor) ca = &black;
            queue->AppendQuad(va,ta,ca);
        }
        
        void Clear();
        void EmptyQueues();
        void Render();
                
        bool ignoreColor;

        protected:        
        friend class Singleton<RenderingEngine>;
        quad_colors black;
        QueueMap queues;
    };
    
}

#endif

