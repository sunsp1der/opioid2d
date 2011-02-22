
#include "util.hpp"
#ifdef DARWIN
#include <gl.h>
#else
#include <GL/gl.h>
#endif

#include <limits.h>
#include <algorithm>
#include "layer.hpp"
#include "node.hpp"
#include "rendering.hpp"
#include "debug.hpp"

#ifndef NULL
#define NULL 0
#endif

namespace opi2d
{
    Layer::Layer(const std::string& name)
    : camera_offset(1.0), camera_rotation(1.0), camera_zoom(1.0),
    ignore_camera(false), name(name), freeform(false) {}
    
    Layer::~Layer()
    {FUNC
        for(Nodes::iterator i=nodes.begin();i != nodes.end(); ++i)
        {
            (*i)->layer = NULL;
            (*i)->Delete();
        }
        this->ResetRenderingPasses();
        this->nodes.clear();
    }
    
    void Layer::ResetRenderingPasses()
    {
        for(RenderingPasses::iterator i=passes.begin(); i != passes.end(); ++i)
        {
            delete (*i);
        }
        this->passes.clear();
    }
    
    void Layer::AddNode(Node *node)
    {FUNC
        this->nodes.push_back(node);
    }
    
    void Layer::RemoveNode(Node* node)
    {FUNC
        this->nodes.remove(node);
    }

    void Layer::SendNodeToTop(Node* node)
    {
	    this->nodes.remove( node);
	    this->nodes.push_back( node);
    }

    void Layer::SendNodeToBottom(Node* node)
    {
	    this->nodes.remove( node);
	    this->nodes.push_front( node);
    }


    std::list<Node*> Layer::GetNodes()
    {
	    return this->nodes;
    }

    void Layer::SetNodes( std::list<Node*> nodes)
    {
	    this->nodes = nodes;
    }

    void Layer::AddRenderingPass(RenderingPass* pass)
    {
        this->passes.push_back(pass);
    }
    
    void Layer::SetFreeForm(bool flag)
    {
    	this->freeform = flag;
    }
    
    void Layer::Render()
    {FUNC
    	if (freeform)
    	{
    		this->RenderFree();
    		return;
    	}
        RenderingEngine* engine = RenderingEngine::GetInstance();
        int zorder = 0;
        for(Nodes::iterator i=this->nodes.begin();i != this->nodes.end(); ++i)
        {
            (*i)->Traverse(zorder);
        }
        if (this->passes.size() == 0)
        {
            engine->Render();
        }
        else
        {
            for(RenderingPasses::iterator i=passes.begin(); i != passes.end(); ++i)
            {
                (*i)->Apply();
                engine->Render();
            }
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
        }
        engine->EmptyQueues();
    }
    
    void Layer::RenderFree()
    {
        if (this->passes.size() == 0)
        {
	        for(Nodes::iterator i=this->nodes.begin();i != this->nodes.end(); ++i)
	        {
	            (*i)->TraverseFree();
	        }
        }
        else
        {
            for(RenderingPasses::iterator p=passes.begin(); p != passes.end(); ++p)
            {
                (*p)->Apply();
		        for(Nodes::iterator i=this->nodes.begin();i != this->nodes.end(); ++i)
		        {
		            (*i)->TraverseFree();
		        }
            }
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
        }
    }
    
    Sprite* Layer::Pick(const Vec2& p)
    {
    	Sprite* result = NULL;
        for(Nodes::iterator i=this->nodes.begin();i != this->nodes.end(); ++i)
        {
            result = (*i)->Pick(p);
            if (result != NULL) return result;
        }
        return NULL;
    }
    
    RenderingPass::RenderingPass() : src_func(GL_SRC_ALPHA), dst_func(GL_ONE_MINUS_SRC_ALPHA)
    {
    }
    
    void RenderingPass::SetSrcFunc(int func)
    {
        this->src_func = func;
    }

    void RenderingPass::SetDstFunc(int func)
    {
        this->dst_func = func;
    }
    
    void RenderingPass::Apply()
    {
        glBlendFunc(this->src_func, this->dst_func);
    }

}

