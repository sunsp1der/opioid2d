
#include "node.hpp"
#include "layer.hpp"
#include "actions.hpp"
#include "debug.hpp"

namespace opi2d
{
    Node::Node() : physics(NULL), layer(NULL), pos(0,0), offset(0,0), scale(1.0,1.0), rotation(0), 
    fChildren(), bChildren(), parent(NULL), color(1,1,1,1), inherit_color(false), oldpos(0,0), 
    pos_update_tick(-1)
    {FUNC
        
    }
   
    void Node::DeleteNodes(Nodes& nodes)
    {FUNC
        for(Nodes::iterator i = nodes.begin(); i != nodes.end(); ++i)
        {
             (*i)->parent = NULL;
             (*i)->Delete();
        }
    }
   
   
    Node::~Node()
    {FUNC
        this->Detach();
        DeleteNodes(this->fChildren);
        DeleteNodes(this->bChildren);
        this->fChildren.clear();
        this->bChildren.clear();
    }
    
    void Node::ReUse()
    {
    	this->Detach();
        this->pos.set(0,0);
        this->offset.set(0,0);
        this->scale.set(1.0,1.0);
        this->rotation = 0;
        DeleteNodes(this->fChildren);
        DeleteNodes(this->bChildren);
        this->fChildren.clear();
        this->bChildren.clear();
        this->color.set(1,1,1,1);
        this->inherit_color = false;
        this->physics = NULL;
        Identified::ReUse();
    }
    
    void Node::SetColor(float r, float g, float b, float a)
    {FUNC
        this->color.set(r,g,b,a);
    }
    
    
    void Node::Delete()
    {FUNC
        this->Detach();
        DeleteNodes(this->fChildren);
        DeleteNodes(this->bChildren);
        this->fChildren.clear();
        this->bChildren.clear();
        this->physics = NULL;
        Identified::Delete();
    }
    
    void Node::Place(Layer* layer)
    {FUNC
    	if (this->parent != NULL)
    	{
			this->parent->OnDetach(this);
        	this->parent = NULL;
    	}
    	if (this->layer != NULL)
    	{
    		this->layer->RemoveNode(this);
    	}
    	layer->AddNode(this);
        this->layer = layer;
    }
    
    void Node::OnAttach(Node* child, bool back)
    {FUNC
        if (back)
        {
             this->bChildren.push_back(child);
        }
        else
        {
             this->fChildren.push_back(child);
        }
    }
   
    void Node::OnDetach(Node* child)
    {FUNC
        this->fChildren.remove(child);
        this->bChildren.remove(child);
    }
   
    Node* Node::AttachTo(Node* parent, bool back)
    {FUNC
    	if (this->layer != NULL)
    	{
    		this->layer->RemoveNode(this);
    	}
        if (this->parent != NULL)
        {
             this->parent->OnDetach(this);
        }
        this->parent = parent;
        parent->OnAttach(this, back);
        return this;
    }
   
    Node* Node::Detach()
    {FUNC
        if (this->layer != NULL)
        {
            this->layer->RemoveNode(this);
            this->layer = NULL;
        }
        if (this->parent == NULL)
        {
             return this;
        }
        this->parent->OnDetach(this);
        this->parent = NULL;
        return this;
    }

	Layer* Node::GetRootLayer() const
	{
		if (this->layer != NULL) return this->layer;
		if (this->parent == NULL) return NULL;
		return this->parent->GetRootLayer();
	}

	void Node::ToThisFrame(Vec2& p) const
	{
		this->GetTransformationMatrix().transform(p);
	}
	
	void Node::ToParentFrame(Vec2& p) const
	{
		if (this->parent == NULL) return;
		this->parent->GetTransformationMatrix().transform(p);
	}
	
	void Node::FromThisFrame(Vec2& p) const
	{
		this->GetTransformationMatrix().inversed().transform(p);
	}
	
	void Node::FromParentFrame(Vec2& p) const
	{
		if (this->parent == NULL) return;
		this->parent->GetTransformationMatrix().inversed().transform(p);
	}

   
    Sprite* Node::Pick(const Vec2& p)
    {
   		Sprite* result = NULL;
        for(Nodes::iterator i=fChildren.begin(); i != fChildren.end(); ++i)
        {
        	result = (*i)->Pick(p);       
            if (result != NULL) return result;
        }
        result = this->PickSelf(p);
        if (result != NULL) return result;
        for(Nodes::iterator i=bChildren.begin(); i != bChildren.end(); ++i)
        {
        	result = (*i)->Pick(p);       
            if (result != NULL) return result;
        }
        return NULL;   	
    }
   
    Sprite* Node::PickSelf(const Vec2& p)
    {
    	return NULL;
    }
   
    void Node::Traverse(int& zorder)
    {//FUNC
    	this->tcolor.set(this->color);
    	if (this->inherit_color && this->parent != NULL)
    	{
    		this->tcolor *= this->parent->tcolor;
    	}
        for(Nodes::iterator i=bChildren.begin(); i != bChildren.end(); ++i)
            (*i)->Traverse(zorder);
        ++zorder;
    	this->zorder = zorder;
    	this->oldpos.set(this->GetWorldPos());
        this->Enter();
        for(Nodes::iterator i=fChildren.begin(); i != fChildren.end(); ++i)
            (*i)->Traverse(zorder);
    }
    
    void Node::TraverseFree()
    {
    	this->tcolor.set(this->color);
    	if (this->inherit_color && this->parent != NULL)
    	{
    		this->tcolor *= this->parent->tcolor;
    	}
        for(Nodes::iterator i=bChildren.begin(); i != bChildren.end(); ++i)
            (*i)->TraverseFree();
    	this->oldpos.set(this->GetWorldPos());
        this->EnterFree();
        for(Nodes::iterator i=fChildren.begin(); i != fChildren.end(); ++i)
            (*i)->TraverseFree();
    }   
   
    void Node::Enter()
    {//FUNC
    }
    
    void Node::EnterFree()
    {
    }
   
}
