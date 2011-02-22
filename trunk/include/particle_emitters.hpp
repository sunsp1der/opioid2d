
#ifndef OPIPARTICLE_EMITTERS
#define OPIPARTICLE_EMITTER

#include "util.hpp"
#include "vec.hpp"
#include "num.hpp"
#include "identified.hpp"

namespace opi2d
{
	class Node;
	class Image;
	class Particle;
	class ParticleSystem;

    class DLLEXPORT EmitterParameter
    {
    	public:    	
    	virtual floatval Evaluate() = 0;
    	virtual ~EmitterParameter() {}
    	
    	protected:
    };
    
    class ParticleEmitterAction;
    
    class DLLEXPORT ParticleEmitter : public Identified
    {
    	public:
    	ParticleEmitter();
    	virtual ~ParticleEmitter();
    	
    	virtual void Delete();
    	
    	void SetSystem(ParticleSystem* system);
    	void AttachTo(Node* node);
    	void SetPosition(const Vec2& pos);
    	
    	virtual void InitFrom(ParticleEmitter* tmpl);
    	
    	virtual void EmitSingle();
    	virtual void EmitPulse();
    	virtual void Start();
    	
    	virtual void PSetPosition();
    	virtual void PSetDirection();
    	virtual void PSetVelocity();
    	virtual void PSetAcceleration();
    	virtual void PSetRotation();
    	virtual void PSetScale();
    	virtual void PSetLife();
    	virtual void PSetColor();
    	virtual void PSetImage();
    	
    	// emitter parameters

		/*00*/ Image* image;
		/*01*/ EmitterParameter* direction;
		/*02*/ EmitterParameter* angle;
		/*03*/ EmitterParameter* speed;
		/*04*/ EmitterParameter* acceleration_x;
		/*05*/ EmitterParameter* acceleration_y;
		/*06*/ EmitterParameter* friction;
		/*07*/ EmitterParameter* rotation;
		/*08*/ EmitterParameter* rotation_delta;
		/*09*/ EmitterParameter* offset_x;
		/*10*/ EmitterParameter* offset_y;
		/*11*/ EmitterParameter* advance;
		/*12*/ EmitterParameter* scale;
		/*13*/ EmitterParameter* scale_delta;
		
		/*14*/ EmitterParameter* color_red;
		/*15*/ EmitterParameter* color_green;
		/*16*/ EmitterParameter* color_blue;
		/*17*/ EmitterParameter* color_alpha;

		/*18*/ EmitterParameter* color_delta_red;
		/*19*/ EmitterParameter* color_delta_green;
		/*20*/ EmitterParameter* color_delta_blue;
		/*21*/ EmitterParameter* color_delta_alpha;

		/*22*/ EmitterParameter* color_target_red;
		/*23*/ EmitterParameter* color_target_green;
		/*24*/ EmitterParameter* color_target_blue;
		/*25*/ EmitterParameter* color_target_alpha;
		
		/*26*/ EmitterParameter* life;
		/*27*/ EmitterParameter* fade_time;
		/*28*/ EmitterParameter* fade_delay;
		/*29*/ EmitterParameter* fade_in;
		
		/*30*/ EmitterParameter* num_emits;
		/*31*/ EmitterParameter* num_particles;
		
		/*32*/ EmitterParameter* emit_delay;
		/*33*/ EmitterParameter* emits_per_sec;
		/*34*/ EmitterParameter* duration;
		
		/*35*/ EmitterParameter* node_velocity;

		bool align_to_direction;
		bool align_to_node;
		bool rotate_to_node;    	

    	protected:
    	friend class ParticleEmitterAction;
    	ParticleSystem* system;
    	Node* node;
    	Vec2 pos;
    	
    	Particle* p; // current particle that we are emitting
    	
    	ParticleEmitterAction* action;
    	
    	floatval p_dir;
    	int p_num;
    	int emit_num;
    };
    
    class DLLEXPORT PointEmitter : public ParticleEmitter
    {
    	public:
    	
    	virtual void EmitSingle();
    	virtual void PSetPosition();
    	virtual void PSetVelocity();
    	virtual void PSetRotation();
    	virtual void PSetScale();
    	virtual void PSetLife();
    	virtual void PSetColor();
    	virtual void PSetImage();
    };
        
    class DLLEXPORT ConstParameter : public EmitterParameter
    {
    	public:
    	
    	ConstParameter(floatval value) { this->value = value; }
    	floatval Evaluate() { return this->value; }
    	
    	protected:
    	
    	floatval value;
    };
    
    class DLLEXPORT RandomParameter : public EmitterParameter
    {
    	public:
    	RandomParameter(floatval minval, floatval maxval);
    	floatval Evaluate();
    	
    	protected:
    	floatval minval, delta;
    };
    
    class DLLEXPORT VecParameter
    {
    	public:
    	VecParameter(EmitterParameter* paramx, EmitterParameter* paramy);
    	virtual ~VecParameter();
    	Vec2 Evaluate();
    	
    	protected:
    	EmitterParameter* paramx;
    	EmitterParameter* paramy;    	    	
    };
    
    class DLLEXPORT LinearParameter : public EmitterParameter
    {
    	public:
    	floatval Evaluate();
    };
    
    class DLLEXPORT SineParameter : public EmitterParameter
    {
    	public:
    	floatval Evaluate();
    };

	
	
}

#endif

