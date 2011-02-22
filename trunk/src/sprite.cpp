
#include "util.hpp" 

#ifdef DARWIN
#include <gl.h>
#else
#include <GL/gl.h>
#endif
 
#include "sprite.hpp"
#include "rendering.hpp"
#include "num.hpp"
#include "image.hpp"
#include "debug.hpp"
#include "scene.hpp"
#include "director.hpp"
#include "opivm.hpp"
#include "physics.hpp"

#include <iostream>

#ifndef NULL
#define NULL 0
#endif

namespace opi2d
{
	void Sprite::VM_GetProp(ExecFrame* f, int idx)
	{
		switch(idx)
		{
			case 0: // position
				f->pushp(&this->GetPos());
				break;
			case 1: // velocity
				f->pushp(&this->physics->velocity);
				break;
			case 2: // acceleration
				f->pushp(&this->physics->acceleration);
				break;
			case 3: // friction
				f->pushf(this->physics->friction);
				break;
			case 4: // rotation
				f->pushf(this->GetRotation());
				break;
			case 5: // rotation_speed
				f->pushf(this->physics->rotation);
				break;
			case 6: // scale
				f->pushp(&this->GetScale());
				break;
			case 7: // world_position
				f->pushv(this->GetWorldPos());
				break;
		}
	}
	
	void Sprite::VM_SetProp(ExecFrame* f, int idx)
	{
		Vec2* v;
		floatval fv;
		switch(idx)
		{
			case 0: // position
				v = f->popv(); 
				this->GetPos().set(*v);
				break;
			case 1: // velocity
				v = f->popv();
				this->physics->velocity.set(*v);
				break;
			case 2: // acceleration
				v = f->popv();
				this->physics->acceleration.set(*v);
				break;
			case 3: // friction
				fv = f->popf();
				this->physics->friction = fv;
				break;
			case 4: // rotation
				fv = f->popf();
				this->SetRotation(fv);
				break;
			case 5: // rotation_speed
				fv = f->popf();
				this->physics->rotation = fv;
				break;
			case 6: // scale
				v = f->popv();
				this->GetScale().set(*v);
				break;
			case 7: // world_position
				break;
		}		
	}
	
	void Sprite::VM_MetCall(ExecFrame* f, int idx)
	{
		switch(idx)
		{
			case 0: // delete
				this->Delete();
				break;
		}
	}
	
	
    Sprite::Sprite(const Image* image) : Node(), lighting_detail(0), enable_lighting(false), image(image), coll_transform_tick(0)
    {FUNC
    }
    
    void Sprite::ReUse()
    {        
        for(GroupSet::iterator i=groups.begin(); i != groups.end(); ++i)
        {
            (*i)->RemoveSprite(this);
        }
        this->groups.clear();        
        Node::ReUse();
    }
    
    Sprite::~Sprite()
    {FUNC
        /*for(GroupSet::iterator i=groups.begin(); i != groups.end(); ++i)
        {
            (*i)->RemoveSprite(this);
        }
        this->groups.clear();*/        
    }
               
    void Sprite::SetImage(const Image* image)
    {FUNC
        this->image = image;
    }

    void Sprite::CalculateQuad(floatval x, floatval y, const Image* image, quad_vertices& va, quad_vertices& ta, quad_colors& ca) const
    {
        int w = image->w;
        int h = image->h;
               
        va.pts[0].set(x, y);
        va.pts[1].set(x+w,y);
        va.pts[2].set(x+w,y+h);
        va.pts[3].set(x,y+h);
                
        tmat.transform(va.pts[0]);
        tmat.transform(va.pts[1]);
        tmat.transform(va.pts[2]);
        tmat.transform(va.pts[3]);
               
        ta.pts[0].set(image->tx, image->ty);
        ta.pts[1].set(image->txx, image->ty);
        ta.pts[2].set(image->txx, image->tyy);
        ta.pts[3].set(image->tx, image->tyy);
        
        if (enable_lighting)
        {
            Scene* scene = Director::GetInstance()->GetScene();
            for(int i=0; i<4; ++i)
                ca.rgba[i] = scene->CalculateLight(va.pts[i]) * color;
        }
        else            
        {
            ca.rgba[0] = tcolor;
            ca.rgba[1] = tcolor;
            ca.rgba[2] = tcolor;
            ca.rgba[3] = tcolor;
        }
    }

	void Sprite::RenderQuad(floatval x, floatval y, const Image* image, quad_vertices& va, quad_vertices& ta, quad_colors& ca) const
    {
		this->CalculateQuad(x, y, image, va, ta, ca);
        RenderingEngine::GetInstance()->AppendQuad(zorder, image->texid, &va, &ta, &ca);   
    }

	void Sprite::RenderFree(floatval x, floatval y, const Image* image, quad_vertices& va, quad_vertices& ta, quad_colors& ca) const
    {
		this->CalculateQuad(x, y, image, va, ta, ca);
        glBindTexture(GL_TEXTURE_2D, image->texid);
        glBegin(GL_QUADS);
        for(int i=0;i<4;++i)
        {
	        glColor4f(ca.rgba[i].red, ca.rgba[i].green, ca.rgba[i].blue, ca.rgba[i].alpha);
	        glTexCoord2f(ta.pts[i].x, ta.pts[i].y);
	        glVertex2f(va.pts[i].x, va.pts[i].y);
        } 
        glEnd();
    }

    void Sprite::EnterFree()
    {
    	// TODO: copy/pasted from Sprite::Enter. Need to refactor to make common
    	// parts reusable between the two functions.
        if (this->image == NULL)
        {
            return;
        }
        if (pos_update_tick != Director::GetInstance()->GetTickID())
        {
            this->update_world_pos();
        }

        quad_vertices va;
        quad_vertices ta;
        quad_colors ca;
       
        const Vec2& hotspot = image->hotspot;
        int w = image->w;
        int h = image->h;
        floatval x = -hotspot.x*w;
        floatval y = -hotspot.y*h;


        if (!this->image->IsGrid())
        {
            this->RenderFree(x,y,this->image, va,ta,ca);
        }
        else
        {
            // TODO: optimize lighting calculation for the grid
            //       i.e. eliminate the redundant double calculations
            GridImage* gridimg = (GridImage*)this->image;
            DEBUG("gridimg->images");
            Image** imgptr = gridimg->images;
            floatval gy = y;
            int prevh;
            Image* img = (*imgptr);
            for(int row=0;row<gridimg->rows;++row)
            {
                floatval gx = x;
                DEBUG("img->h");
                prevh = img->h;
                for(int col=0;col<gridimg->cols;++col)
                {
                    DEBUG("RenderQuad");
                    this->RenderFree(gx,gy,img,va,ta,ca);
                    gx += img->w;
                    ++imgptr;
                    img = (*imgptr);
                }
                gy += prevh;
            }
        }
    }
    
    void Sprite::Enter()
    {//FUNC
        if (this->image == NULL)
        {
            return;
        }
        if (pos_update_tick != Director::GetInstance()->GetTickID())
        {
            this->update_world_pos();
        }

        quad_vertices va;
        quad_vertices ta;
        quad_colors ca;
       
        const Vec2& hotspot = image->hotspot;
        int w = image->w;
        int h = image->h;
        floatval x = -hotspot.x*w;
        floatval y = -hotspot.y*h;


        if (!this->image->IsGrid())
        {
            this->RenderQuad(x,y,this->image, va,ta,ca);
        }
        else
        {
            // TODO: optimize lighting calculation for the grid
            //       i.e. eliminate the redundant double calculations
            GridImage* gridimg = (GridImage*)this->image;
            DEBUG("gridimg->images");
            Image** imgptr = gridimg->images;
            floatval gy = y;
            int prevh;
            Image* img = (*imgptr);
            for(int row=0;row<gridimg->rows;++row)
            {
                floatval gx = x;
                DEBUG("img->h");
                prevh = img->h;
                for(int col=0;col<gridimg->cols;++col)
                {
                    DEBUG("RenderQuad");
                    this->RenderQuad(gx,gy,img,va,ta,ca);
                    gx += img->w;
                    ++imgptr;
                    img = (*imgptr);
                }
                gy += prevh;
            }
        }
            
    }
    
    void Sprite::Delete()
    {FUNC
        for(GroupSet::iterator i=groups.begin(); i != groups.end(); ++i)
        {
            (*i)->RemoveSprite(this);
        }
        this->groups.clear();        
        Node::Delete();
    }
    
    void Sprite::JoinGroup(SpriteGroup* group)
    {
        group->AddSprite(this);
        this->groups.insert(group);
    }
    
    void Sprite::LeaveGroup(SpriteGroup* group)
    {FUNC
        group->RemoveSprite(this);
        this->groups.erase(group);
    }
        
    void Sprite::TransformCollisionNodes()
    {
    	if (this->image == NULL) return;
        int now = Director::GetInstance()->GetTickID();
        if (this->coll_transform_tick == now) return;
        this->coll_transform_tick = now;
    	this->collnodes.clear();
        const Mat9& mat = this->GetTransformationMatrix();
        Vec2 nodepos(-(image->hotspot));
        nodepos.mul(image->w, image->h);
        //nodepos.add(this->GetPos());
        //hotspot.add(this->GetWorldPos());
        if (image->nodes.size() == 0)
        {
            CollisionNode node(0,0,image->w,image->h);
            node.center += nodepos; 
            mat.transform(node.center);
            node.size.mul(this->scale);
            node.size.xyabs();
            this->collnodes.push_back(node);
            return;
        }                                    
        for(CollisionNodes::const_iterator col=image->nodes.begin(); col != image->nodes.end(); ++col)
        {        	
            CollisionNode node(*col);
            node.center += nodepos; 
            mat.transform(node.center);
            node.size.mul(this->scale);
            node.size.xyabs();
            this->collnodes.push_back(node);
        }
    }
    
    Rect Sprite::GetRect() const
    {
    	Rect r;
    	floatval w,h;
    	Vec2 hotspot;
    	if (this->image == NULL)
    	{
    		w = h = 0;
    		hotspot.set(0,0);
    	}
    	else
    	{
    		w = image->w;
    		h = image->h;
    		hotspot.set(image->hotspot);
    	}
    	w *= this->scale.x;
    	h *= this->scale.y;
    	const Vec2& wpos = this->GetPos();
    	floatval x = wpos.x - w * hotspot.x;
    	floatval y = wpos.y - h * hotspot.y;
    	r.topleft.set(x,y);
    	r.size.set(w,h);
    	return r;
    }
    
    Rect Sprite::GetWorldRect() const
    {
    	Rect r;
    	floatval w,h;
    	Vec2 hotspot;
    	if (this->image == NULL)
    	{
    		w = h = 0;
    		hotspot.set(0,0);
    	}
    	else
    	{
    		w = image->w;
    		h = image->h;
    		hotspot.set(image->hotspot);
    	}
    	w *= this->scale.x;
    	h *= this->scale.y;
    	const Vec2& wpos = this->GetWorldPos();
    	floatval x = wpos.x - w * hotspot.x;
    	floatval y = wpos.y - h * hotspot.y;
    	r.topleft.set(x,y);
    	r.size.set(w,h);
    	return r;
    }
    
    FreeRect Sprite::GetTransformedRect() const
    {
    	Rect r;
    	floatval w,h;
    	Vec2 hotspot;
    	if (this->image == NULL)
    	{
    		w = h = 0;
    		hotspot.set(0,0);
    	}
    	else
    	{
    		w = image->w;
    		h = image->h;
    		hotspot.set(image->hotspot);
    	}
    	floatval x = -w * hotspot.x;
    	floatval y = -h * hotspot.y;
    	r.topleft.set(x,y);
    	r.size.set(w,h);
    	return GetTransformationMatrix().transform(r);
    }
    
    Sprite* Sprite::PickSelf(const Vec2& p)
    {
    	if (this->image != NULL)
    	{
    		/*if (this->rotation == 0.0)
    		{
		    	Rect r = this->GetWorldRect();
		    	if (r.contains(p)) return this;
    		}
    		else
    		{*/
    			FreeRect r = this->GetTransformedRect();
    			if (r.contains(p)) return this;
    		//}
    	}
    	return NULL;
    }
    
    SpriteGroup::SpriteGroup(const std::string& name) : name(name), iterating(false)
    {        
    }
    
    SpriteGroup::~SpriteGroup()
    {FUNC
        for(SpriteSet::iterator i=sprites.begin(); i != sprites.end(); ++i)
        {
            (*i)->LeaveGroup(this);
        }
    }
    
    void SpriteGroup::AddSprite(Sprite* sprite)
    {FUNC
    	if (this->iterating)
    	{
    		this->to_be_added.insert(sprite);
    	}
    	else
    	{
        	this->sprites.insert(sprite);
    	}
    }
    
    void SpriteGroup::RemoveSprite(Sprite* sprite)
    {FUNC
    	if (this->iterating)
    	{
    		this->to_be_deleted.insert(sprite);
    	}
    	else
    	{
        	this->sprites.erase(sprite);
    	}
    }
    
    void SpriteGroup::Tick()
    {
    	floatval delta = Director::GetInstance()->GetTicker().delta / 1000.0;
    	this->Lock();
    	for(mutatorlist::iterator m=mutators.begin(); m != mutators.end(); ++m)
        {
        	(*m)->Mutate(this, delta);
        }
        this->Unlock();
    }
    
    SpriteSet::iterator SpriteGroup::Begin()
    {
        return this->sprites.begin();
    }
    
    SpriteSet::iterator SpriteGroup::End()
    {
        return this->sprites.end();
    }
    
    void SpriteGroup::ClearBuffers()
    {
        for(SpriteSet::iterator i = to_be_deleted.begin(); i != to_be_deleted.end(); ++i)
        {
        	this->sprites.erase(*i);
        }
        to_be_deleted.clear();
        for(SpriteSet::iterator i = to_be_added.begin(); i != to_be_added.end(); ++i)
        {
        	this->sprites.insert(*i);
        }
        to_be_added.clear();
    }
    
    std::vector<Sprite*> SpriteGroup::ListSprites() const
    {
    	std::vector<Sprite*> result;
    	
        for(SpriteSet::const_iterator i = sprites.begin(); i != sprites.end(); ++i)
        {
        	result.push_back(*i);
        }
        return result;
    }
    
    Sprite* SpriteGroup::Pick(const Vec2& p) const
    {
        for(SpriteSet::const_iterator i = sprites.begin(); i != sprites.end(); ++i)
        {
        	Sprite* result = (*i)->PickSelf(p);
        	if (result != NULL) return result;
        }
        return NULL;
    }
    
    void SpriteGroup::AddMutator(Mutator* mutator)
    {
    	this->mutators.push_back(mutator);
    }
}
