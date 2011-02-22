#include <iostream>
#include <cmath>

#include "actions.hpp"
#include "director.hpp"
#include "scene.hpp"
#include "node.hpp"
#include "sprite.hpp"
#include "debug.hpp"
#include "node.hpp"
#include "particles.hpp"
#include "particle_emitters.hpp"
#include "num.hpp"

namespace opi2d
{
    ActionManager::~ActionManager()
    {FUNC
        for(ActionSet::iterator i = to_be_deleted.begin(); i != to_be_deleted.end(); ++i)
        {
            actions.erase(*i);
        }
        to_be_deleted.clear();
        
        // temporary solution to prevent the container from changing size while iterating
        ActionSet copy(actions);
        for(ActionSet::iterator i = copy.begin(); i != copy.end(); ++i)
        {
            (*i)->Delete();
        }                
        for(ActionSet::iterator i = new_actions.begin(); i != new_actions.end(); ++i)
        {
            (*i)->Delete();
        }
        new_actions.clear();
    }
    
    void ActionManager::AddAction(Action* action)
    {FUNC
        new_actions.insert(action);
    }
    
    void ActionManager::RemoveAction(Action* action)
    {FUNC
    	//std::cout << "remove request for " << (int)action << std::endl;
       	action->Delete();
        to_be_deleted.insert(action);
    }
    
    void ActionManager::Iterate()
    {FUNC
        Director* d = Director::GetInstance();
        double delta = d->GetTicker().delta;
        //int now = d->GetTicker().now;
        //std::cout << "start to_be_deleted cleanup #1" << std::endl;
        if (to_be_deleted.size() > 0)
        {
            for(ActionSet::iterator i = to_be_deleted.begin(); i != to_be_deleted.end(); ++i)
            {
            	//std::cout << "removing " << (int)(*i) << std::endl;
                actions.erase(*i);
            }
            to_be_deleted.clear();
        }
        //std::cout << "start new_actions insert #1" << std::endl;
        if (new_actions.size() > 0)
        {
            for(ActionSet::iterator i = new_actions.begin(); i != new_actions.end(); ++i)
            {
                actions.insert(*i);
            }
            new_actions.clear();
        }
        //std::cout << "iterate actions" << std::endl;
        for(ActionSet::iterator i = actions.begin(); i != actions.end(); ++i)
        {
            Action* action = (*i);
            action->CommonTick(delta);
        }
        //std::cout << "start to_be_deleted cleanup #2" << std::endl;
        if (to_be_deleted.size() > 0)
        {
            for(ActionSet::iterator i = to_be_deleted.begin(); i != to_be_deleted.end(); ++i)
            {
            	//(*i)->Delete();
                actions.erase(*i);
            }
            to_be_deleted.clear();
        }
        //std::cout << "start new_actions insert #2" << std::endl;
        if (new_actions.size() > 0)
        {
            for(ActionSet::iterator i = new_actions.begin(); i != new_actions.end(); ++i)
            {
                actions.insert(*i);
            }
            new_actions.clear();
        }

    }
       
    Action::Action() : target(NULL), callbacks(NULL), time_elapsed(0), time_limit(-1)
    {FUNC
    	Scene* scene = Director::GetInstance()->GetScene();
    	if (scene != NULL)
    	{
        	scene->AddAction(this);
    	}
    }
    
    // Action destructor is implemented just for debugging's sake so that it
    // is easier to trace when action objects are deleted.
    Action::~Action()
    {FUNC
        
    }
    
    void Action::Setup(Node* node, ActionCallbacks* callbacks)
    {
        this->target = node;
        this->callbacks = callbacks;
    }
    
    void Action::SetTimeLimit(double secs)
    {FUNC
        this->time_limit = secs;
    }
    
    void Action::End()
    {FUNC
    	//std::cout << "ending action " << (int)(this) << std::endl;
    	Scene* scene = Director::GetInstance()->GetScene();
    	if (scene != NULL)
    	{ 
        	scene->RemoveAction(this);
    	}
        if (this->callbacks != NULL) callbacks->End();
    }
    
    void Action::CommonTick(double delta)
    {
    	this->time_elapsed += delta;
        if (this->IsDeleted() || (this->target != NULL && this->target->IsDeleted()))
        {
        	Director::GetInstance()->GetScene()->RemoveAction(this);
            return;
        }
        if (this->time_limit > -1 && this->time_elapsed >= this->time_limit)
        {
            this->End();
            return;
        }
        this->Tick(delta);
    }


    IntervalAction::IntervalAction() : interval_time(0), repeat_mode(0), smooth(false) {}
    
    void IntervalAction::SetInterval(double secs, int repeatMode)
    {FUNC
        this->interval_time = secs;
        this->repeat_mode = repeatMode;
    }    
    
    double IntervalAction::GetIntervalTime()
    {FUNC
        double time = time_elapsed / interval_time;
        switch(repeat_mode)
        {
        case STOPMODE:
            if (time > 1.0) 
            {
                this->End();
                return 1.0;
            }
            return time;
        case REPEATMODE:
            return time - floor(time);
        case PINGPONGMODE:
            time = fmod(time, 2.0);
            if (time > 1.0) return 1 - (time - floor(time));
            return time;
        }
        // should never come here as the mode parameter is validated in Python API
        // TODO: assertion check
        return 0;
    }
    
    void IntervalAction::SetSmoothing(floatval fadein, floatval fadeout)
    {
    	this->smooth = true;
    	fadein = fadein / this->interval_time;
    	fadeout = 1.0 - fadeout / this->interval_time; 
    	this->smoother.init(fadein, fadeout);
    }
    
    void IntervalAction::Tick(double delta)
    {FUNC
        //time_elapsed += delta;
        double t = GetIntervalTime();
        if (this->smooth) t = this->smoother.calc(t);
        IntervalTick(t);
    }
    
    SmoothInterval::SmoothInterval()
    {
    }
    
    void SmoothInterval::init(floatval tr, floatval ts)
    {
    	if (tr < 0) tr = 0;
    	if (tr > 1) tr = 1;
    	if (ts > 1) ts = 1;
    	if (ts < tr) ts = tr;
    	this->tr = tr;
    	this->ts = ts;
    	
    	// pre-calculate intermediate values
    	c = 2.0/(ts-tr+1);
    	floatval c2 = 0.5*c;
    	if (tr > 0) c2tr = c2/tr;
    	trc2 = tr*c2;
    	if (ts < 1.0)
    	{
    		floatval d = (1-ts);
    		cd = c/d;
    		c2d = -c2/d;
    	}
    }
    
    floatval SmoothInterval::calc(floatval t)
    {
    	if (t < tr)
    	{
    		return c2tr*t*t;
    	}
    	else if (t > ts)
    	{
    		return c2d*t*t+cd*t+c2d+1;
    	}
    	else
    	{
    		return c*t-trc2;
    	}
    }
        
    Move::Move(const Vec2& velocity) : velocity(velocity)
    {}
    
    void Move::Tick(double delta)
    {
        target->GetPos().add(delta*velocity.x, delta*velocity.y);
    }
    
    void Move::SetVelocity(const Vec2& velocity)
    {
        this->velocity = velocity;
    }
    
    void Move::AddVelocity(const Vec2& velocity)
    {
        this->velocity += velocity;
    }
    
    void Move::MulVelocity(floatval multiplier)
    {
        this->velocity *= multiplier;
    }
    
    MoveDelta::MoveDelta(const Vec2& delta) :
    delta(delta)
    {        
    }
    
    void MoveDelta::Start()
    {
        start_pos = target->GetPos();
    }
    
    void MoveDelta::IntervalTick(double itime)
    {
        target->GetPos().set(start_pos + delta * itime);
    }
    
    MoveTo::MoveTo(const Vec2& pos) : MoveDelta(pos)
    {        
    }
    
    void MoveTo::Start()
    {
        MoveDelta::Start();
        delta = delta - start_pos;
    }
    
    AlphaFade::AlphaFade(float dstAlpha) : end_alpha(dstAlpha)
    {
    }
    
    void AlphaFade::Start()
    {
        start_alpha = target->GetColor().alpha;
        delta_alpha = end_alpha - start_alpha;
    }
    
    void AlphaFade::IntervalTick(double itime)
    {
        float alpha = start_alpha + delta_alpha * itime;
        target->GetColor().alpha = alpha;
    }


    ColorFade::ColorFade(const Color& color) : end_color(color)
    {
    }
    
    void ColorFade::Start()
    {
        start_color = target->GetColor();
        delta_color = end_color - start_color;
    }
    
    void ColorFade::IntervalTick(double itime)
    {
        target->GetColor().set(start_color + delta_color * itime);
    }

    
    Delay::Delay(double secs) : time_left(secs)
    {
    }
    
    void Delay::Tick(double delta)
    {
        this->time_left -= delta;
        if (time_left <= 0)
        {
            this->End();
        }
    }
    
    RotateDelta::RotateDelta(floatval delta) : delta(delta)
    {
    }
    
    void RotateDelta::Start()
    {
        this->start_pos = this->target->GetRotation();
    }
    
    void RotateDelta::IntervalTick(double itime)
    {
        this->target->SetRotation(start_pos + itime * delta);
    }
    
    Rotate::Rotate(floatval speed) : speed(speed)
    {
    }
    
    void Rotate::Tick(double delta)
    {
        this->target->SetRotation(target->GetRotation() + delta * this->speed);
    }
    
    Scale::Scale(floatval speed, bool multiply) : speed(speed), multiply(multiply)
    {
    }
    
    void Scale::Tick(double delta)
    {
        if (this->multiply)
        {
            const floatval v = powf(this->speed, delta);
            this->target->GetScale().mul(v);
        }
        else
        {
            const floatval v = delta * this->speed;
            this->target->GetScale().add(v, v);
        }
    }
	
	ScaleTo::ScaleTo(const Vec2& dstScale) : end_scale(dstScale)
	{
	}
	
	void ScaleTo::Start()
	{
		start_scale = target->GetScale();
		delta_scale = end_scale - start_scale;
    }
	
	void ScaleTo::IntervalTick(double itime)
	{
		Vec2 scale = start_scale + delta_scale * itime;
		target->SetScale(scale);
	}
	
	
    TickFunc::TickFunc(bool onlyReal) : only_real(onlyReal)
    {
    }
    
    void TickFunc::Tick(double delta)
    {
        if (only_real && !Director::GetInstance()->GetTicker().realTick)
        {
            return;
        }
        if (this->callbacks != NULL) callbacks->Wake();    
    }
    
    FollowPath::FollowPath(int numpoints, floatval lead, bool alignnode)
    : curve(numpoints, lead), alignnode(alignnode), speed(0)
    {
    }
    
    void FollowPath::SetPoint(int i, const Vec2& pt)
    {
        curve.SetPoint(i, pt);
    }
    
    void FollowPath::SetSpeed(floatval speed)
    {
        this->speed = speed;
    }
    
    void FollowPath::Start()
    {
        curve.Init();
    }
    
    void FollowPath::Tick(double delta)
    {
        floatval step = delta * speed;
        curve.Tick(step, target->GetPos(), target->GetRotation(), alignnode);
        if (curve.IsFinished()) this->End();
    }
    
    Animate::Animate(double delay)
    : delay(delay), delay_left(delay)
    {
    }
    
    void Animate::SetDelay(double delay)
    {
    	this->delay_left = delay;
    	this->delay = delay;
    }
       	
   	void Animate::Tick(double delta)
   	{
   		this->delay_left -= delta;
   		if (this->delay_left < 0)
   		{
   			this->delay_left += this->delay;
   			this->callbacks->Wake();
   		}
   	}
    	
    
    KeepFacing::KeepFacing(Node* target, int offset)
    {
    	this->dest = target;
    	this->offset = offset;
    }
    
    void KeepFacing::Tick(double delta)
    {
    	Node* parent = this->target->GetParent();
    	Vec2 d;
    	// If the Node has a parent, we have to calculate the direction in the parent's
    	// reference frame. TODO: This needs to be optimized if possible.
    	if (parent != NULL)
    	{
    		const Mat9 mat = parent->GetTransformationMatrix().inversed();
    		Vec2 a(this->dest->GetWorldPos());
    		Vec2 b(this->target->GetWorldPos());
    		mat.transform(a);
    		mat.transform(b);
    		d = a - b;
    	}
    	else
    	{
	    	d = this->dest->GetWorldPos() - this->target->GetWorldPos();
    	}
    	this->target->SetRotation(d.direction() + this->offset);
    }
    
    OrbitAround::OrbitAround(Node* center, floatval speed, bool keepAligned)
    : center(center), speed(speed), keepAligned(keepAligned)
    {
    }
    
    void OrbitAround::Start()
    {
    	this->initRotation = this->target->GetRotation();
    	Vec2 v = this->target->GetWorldPos() - this->center->GetWorldPos();
  		this->range = v.length(); 
   		this->begin = v.direction();
    }
    
    void OrbitAround::Tick(double delta)
    {
    	// TODO: fix for reference frame
    	floatval adelta = this->time_elapsed * this->speed;
    	floatval angle = this->begin + adelta;
    	floatval rot = this->initRotation;
    	if (this->keepAligned)
    	{
    		rot += adelta;
    	}
    	this->target->SetRotation(rot);
    	Vec2 pos = this->center->GetWorldPos() + Vec2(angle, this->range).rad2xy();
    	this->target->GetPos().set(pos);
    }
    
    
    ParticleEmitterAction::ParticleEmitterAction(ParticleEmitter* emitter)
    : emitter(emitter), emit_quota(0)
    {    	
    }
    
    void ParticleEmitterAction::Start()
    {
    	this->next_delay = 0;
    	if (this->emitter->num_emits != NULL)
    	{
    		this->num_emits = (int)this->emitter->num_emits->Evaluate();
    	}
    	if (this->emitter->duration != NULL)
    	{
    		this->duration = this->emitter->duration->Evaluate();
    	}
    }
    
    void ParticleEmitterAction::Tick(double delta)
    {
    	ParticleEmitter* e = this->emitter;
    	if (e->node != NULL && e->node->IsDeleted())
    	{
    		this->End();
    		return;
    	}
    	if (this->emitter->duration != NULL)
    	{
    		this->duration -= delta;
    		if (this->duration <= 0)
    		{
    			this->End();
    			return;
    		}
    	}
    	if (e->emit_delay != NULL)
    	{
    		this->next_delay -= delta;
    		if (this->next_delay <= 0)
    		{
    			e->EmitPulse();
    			if (this->emitter->num_emits != NULL && e->emit_num >= this->num_emits)
    			{
    				this->End();
    				return;
    			}
    			this->next_delay += this->emitter->emit_delay->Evaluate();
    		}
    	}
    	else
    	{
    		floatval freq = e->emits_per_sec->Evaluate();
    		this->emit_quota += freq*delta;
    		bool check = (this->emitter->num_emits != NULL);  
    		while (e->emit_num < (int)(this->emit_quota))
    		{
    			e->EmitPulse();
    			if (check && e->emit_num >= this->num_emits)
    			{
    				this->End();
    				return;
    			}
    		}
    	}
    }
    
    void ParticleEmitterAction::Delete()
    {
    	if (this->emitter != NULL)
    	{
    		this->emitter->action = NULL;
    		this->emitter->Delete();
    		this->emitter = NULL;
    	}
    	Action::Delete();
    }
}


