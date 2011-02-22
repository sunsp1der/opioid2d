#include <stdlib.h>
#include "particle_emitters.hpp"
#include "particles.hpp"
#include "actions.hpp"
#include "image.hpp"
#include "physics.hpp"

namespace opi2d
{
	
	    RandomParameter::RandomParameter(floatval minval, floatval maxval)
    {
    	this->minval = minval;
    	this->delta = maxval - minval;
    }
    
    floatval RandomParameter::Evaluate()
    {
    	return this->minval + (this->delta * rand()) / (RAND_MAX + 1.0);
    }
    
    floatval LinearParameter::Evaluate()
    {
    	return 0;
    }
    
    floatval SineParameter::Evaluate()
    {
    	return 0;
    }
    
	VecParameter::VecParameter(EmitterParameter* paramx, EmitterParameter* paramy)
	: paramx(paramx), paramy(paramy)
	{
	}
	
	VecParameter::~VecParameter()
	{
		delete this->paramx;
		delete this->paramy;
	}
	
	Vec2 VecParameter::Evaluate()
	{
		return Vec2();
	}	
    
    ParticleEmitter::ParticleEmitter()
    {
    	this->node = NULL;
    	this->action = NULL;
    	this->system = NULL;
    	this->p = NULL;
    	// set all emitter parameters to NULL
    	memset(&(this->image), 0, 36*sizeof(void*));
    }
    
    void ParticleEmitter::InitFrom(ParticleEmitter* tmpl)
    {
    	memcpy(&(this->image), &(tmpl->image), 36*sizeof(void*) + 3*sizeof(bool));
    }
    
    ParticleEmitter::~ParticleEmitter()
    {
    	if (this->action != NULL)
    	{
    		this->action->End();
    	}
    }
    
    void ParticleEmitter::Delete()
    {
    	if (this->action != NULL)
    	{
    		this->action->End();
    	}
    	Identified::Delete();
    }
       
    void ParticleEmitter::AttachTo(Node* node)
    {
    	this->node = node;
    }
    
    void ParticleEmitter::SetPosition(const Vec2& pos)
    {
    	this->pos.set(pos);
    }
    
    void ParticleEmitter::SetSystem(ParticleSystem* system)
    {
    	this->system = system;
    }
    
    void ParticleEmitter::EmitSingle()
    {
    	this->p = new Particle();
    	this->system->AddParticle(this->p);
    	this->PSetLife();
    	this->PSetDirection();
    	this->PSetPosition();
    	if (this->offset_x != NULL)
    	{
    		floatval ox = this->offset_x->Evaluate();
    		floatval oy = this->offset_y->Evaluate();
    		this->p->pos.add(ox,oy);
    	}
    	this->PSetVelocity();
    	this->PSetAcceleration();
    	if (this->friction != NULL)
    	{
    		this->p->friction = this->friction->Evaluate();
    	}
    	this->PSetRotation();
    	this->PSetScale();
    	this->PSetColor();
    	this->PSetImage();
    }
    
    void ParticleEmitter::EmitPulse()
    {
    	int num = (int)(this->num_particles->Evaluate() + 0.49);
    	for(p_num = 0; p_num < num; ++p_num)
    	{
    		this->EmitSingle();
    	}
    	++this->emit_num;
    }
    
    void ParticleEmitter::Start()
    {
    	this->emit_num = 0;
    	this->action = new ParticleEmitterAction(this);
    	this->action->Start();    	
    }
    
    void ParticleEmitter::PSetPosition()
    {
    	if (this->node == NULL)
    	{
    		this->p->pos.set(this->pos);
    	}
    	else
    	{
    		this->p->pos.set(this->node->GetWorldPos());
    	}
    	if (this->advance != NULL)
    	{
    		this->p->pos += Vec2(this->p_dir, this->advance->Evaluate()).rad2xy();
    	}
    }
    
    void ParticleEmitter::PSetDirection()
    {
    	this->p_dir = this->direction->Evaluate();
    	floatval angle = this->angle->Evaluate();
    	this->p_dir += (angle * rand()) / (RAND_MAX + 1.0) - angle / 2.0;
    	if (this->node != NULL && this->align_to_node)
    	{
    		this->p_dir += this->node->GetRotation();
    	}
    }
    
    void ParticleEmitter::PSetVelocity()
    {
    	floatval speed = this->speed->Evaluate();
    	this->p->velocity.set(Vec2(this->p_dir, speed).rad2xy());
    	if (this->node != NULL && this->node_velocity != NULL && this->node->physics != NULL)
    	{
    		this->p->velocity.add(this->node->physics->velocity * this->node_velocity->Evaluate());
    	}
    }
    
    void ParticleEmitter::PSetAcceleration()
    {
    	if (this->acceleration_x != NULL)
    	{
    		this->p->acceleration.set(this->acceleration_x->Evaluate(), this->acceleration_y->Evaluate());
    	}
    }
    
    void ParticleEmitter::PSetRotation()
    {
    	floatval rot = this->rotation->Evaluate();
    	if (this->align_to_direction)
    	{
    		rot += this->p_dir;
    	}
    	if (this->node != NULL && this->rotate_to_node)
    	{
    		rot += this->node->GetRotation();
    	}
    	this->p->rotation = rot;
    	this->p->rotation_delta = this->rotation_delta->Evaluate();
    }
    
    void ParticleEmitter::PSetScale()
    {
    	this->p->scale = this->scale->Evaluate();
    	this->p->scale_delta = this->scale_delta->Evaluate();
    }
    
    void ParticleEmitter::PSetLife()
    {
    	floatval life = this->life->Evaluate();
    	this->p->life = life;
    	float ft = 0;
    	if (this->fade_delay != NULL)
    	{
    		ft = life - this->fade_delay->Evaluate();
    		if (ft < 0) ft = 0;
    	}
    	else if (this->fade_time != NULL)
    	{
    		ft = this->fade_time->Evaluate();
    	}
    	this->p->fade_time = ft;
    	if (this->fade_in != NULL)
    	{
    		this->p->fade_in = this->fade_in->Evaluate();
    	}
    }
    
    void ParticleEmitter::PSetColor()
    {
    	if (this->color_red != NULL)
    	{
    		this->p->color.set(
    			this->color_red->Evaluate(),
    			this->color_green->Evaluate(),
    			this->color_blue->Evaluate(),
    			this->color_alpha->Evaluate()
    			);
    	}
    	else
    	{
    		this->p->color.set(1,1,1,1);
    	}
    	
    	if (this->color_delta_red != NULL)
    	{
    		this->p->color_delta.set(
    			this->color_delta_red->Evaluate(),
    			this->color_delta_green->Evaluate(),
    			this->color_delta_blue->Evaluate(),
    			this->color_delta_alpha->Evaluate()
    			);
    	}
    	else
    	{
    		this->p->color_delta.set(0,0,0,0);
    	}
    	
    	if (this->color_target_red != NULL)
    	{
    		Color target(
    			this->color_target_red->Evaluate(),
    			this->color_target_green->Evaluate(),
    			this->color_target_blue->Evaluate(),
    			this->color_target_alpha->Evaluate()
    		);
    		this->p->color_delta = (target - this->p->color) / this->p->life;
    	}
    }
    
    void ParticleEmitter::PSetImage()
    {
    	p->image = this->image;
    }    
    
/*
 	void Emitter::EmitSingle()
 	{
 	}
 	
	void Emitter::PSetPosition()
	{
	}
	
	void Emitter::PSetVelocity()
	{
	}
	
	void Emitter::PSetRotation()
	{
	}
	
	void Emitter::PSetScale()
	{
	}
	
	void Emitter::PSetLife()
	{
	}
	
	void Emitter::PSetColor()
	{
	}
	
	void Emitter::PSetImage()
	{
	}
*/

 	void PointEmitter::EmitSingle()
 	{
 	}
 	
	void PointEmitter::PSetPosition()
	{
	}
	
	void PointEmitter::PSetVelocity()
	{
	}
	
	void PointEmitter::PSetRotation()
	{
	}
	
	void PointEmitter::PSetScale()
	{
	}
	
	void PointEmitter::PSetLife()
	{
	}
	
	void PointEmitter::PSetColor()
	{
	}
	
	void PointEmitter::PSetImage()
	{
	}
		
}
