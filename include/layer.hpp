/*
 * Opioid2D - layer
 * Copyright (c) 2006 Sami Hangaslammi <shang@iki.fi>
 * 
 * Defines a single rendering layer on a scene.
 */

#ifndef OPILAYER_HPP
#define OPILAYER_HPP

#include "util.hpp"

#include <set>
#include <list>
#include <string>

#include "num.hpp"
#include "vec.hpp"

namespace opi2d
{
    class Node;
    class Sprite;
    class RenderingPass;

    typedef std::list<RenderingPass*> RenderingPasses;
    
    class Layer
    {
        public:

        Layer(const std::string& name);
        virtual ~Layer();
        
        inline const std::string& GetName() const { return this->name; }
        
        void Render();
        
        void AddNode(Node* node);
        void RemoveNode(Node* node);
        
        void AddRenderingPass(RenderingPass* pass);
        void ResetRenderingPasses();

        void SendNodeToTop(Node* node);
        void SendNodeToBottom(Node* node);
        std::list<Node*> GetNodes();
        void SetNodes( std::list<Node*> nodes);


        void SetFreeForm(bool flag);
        
        Sprite* Pick(const Vec2& p);
        
        floatval camera_offset;
        floatval camera_rotation;
        floatval camera_zoom;
        bool ignore_camera;
        std::list<Node*> nodes;
            
        protected:
        
        void RenderFree();
        
        std::string name;
        RenderingPasses passes;
        bool freeform;
    };
   
    /*class StaticLayer : public Layer
    {
    };
   
    class StabileLayer : public Layer
    {
    };*/
    
    class RenderingPass
    {
        public:
        RenderingPass();
        
        void SetSrcFunc(int func);
        void SetDstFunc(int func);
        void Apply();
        
        protected:
        int src_func;
        int dst_func;
    };
}
   
#endif

