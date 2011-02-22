
#ifndef OPIPARTICLES
#define OPIPARTICLES

#include "util.hpp"

#include <set>
#include <vector>

#include "vec.hpp"
#include "num.hpp"
#include "color.hpp"
#include "node.hpp"
#include "mutators.hpp"

namespace opi2d
{
	class Image;
	
    class DLLEXPORT Particle
    {
        public:
            
        Particle();
        ~Particle() {};        
        
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
        
        floatval age;
        floatval life;
        floatval fade_time;
        floatval fade_in;
        
        Image* image;
    };
    
    typedef std::set<Particle*> particleset;
    
    class DLLEXPORT ParticleSystem : public Node
    {
        public:
        ParticleSystem();
        virtual ~ParticleSystem();
        
        void AddParticle(Particle* particle);
        void AddMutator(Mutator* mutator);
        
        virtual void Enter();
        
        particleset particles;
        particleset to_be_deleted;
        mutatorlist mutators;
        int last_update;
    };

    
}
    
#endif

