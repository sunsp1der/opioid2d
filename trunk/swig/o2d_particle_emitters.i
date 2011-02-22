class EmitterParameter
{
	public:
	
	virtual floatval Evaluate() = 0;
};

class ParticleEmitter : public Identified
{
	public:
	ParticleEmitter();
	virtual ~ParticleEmitter();
	
	virtual void Delete();
	
	void AttachTo(Node* node);
	void SetPosition(const Vec2& pos);
	void SetSystem(ParticleSystem* system);
	
   	virtual void InitFrom(ParticleEmitter* tmpl);	
	
	virtual void EmitSingle();
	virtual void EmitPulse();
	virtual void Start();
		
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
};

class ConstParameter : public EmitterParameter
{
	public:
	
	ConstParameter(floatval value);
	floatval Evaluate();
	
};

class RandomParameter : public EmitterParameter
{
	public:
	RandomParameter(floatval minval, floatval maxval);
	floatval Evaluate();
};

class LinearParameter : public EmitterParameter
{
	public:
	floatval Evaluate();
};

class SineParameter : public EmitterParameter
{
	public:
	floatval Evaluate();
};
