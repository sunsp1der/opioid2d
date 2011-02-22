class Particle
{
public:
        
    Particle();
    ~Particle();
    
    Vec2 pos;
    Vec2 velocity;
    Vec2 acceleration;
    floatval friction;
    
    floatval rotation;
    floatval rotation_delta;
    
    floatval scale;
    floatval scale_delta;
    
    Color color;
    Color color_delta;
    
    floatval life;
    floatval fade_time;
    floatval fade_in;
    
    Image* image;
};

class Mutator;

class ParticleSystem : public Node
{
public:
    ParticleSystem();
    ~ParticleSystem();
    
    void AddParticle(Particle* particle);
    void AddMutator(Mutator* mutator);
};

%include "o2d_particle_emitters.i"

