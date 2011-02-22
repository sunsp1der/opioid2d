
#include <cstdlib>
#include <cstring>

#include "particles.hpp"
#include "mat.hpp"
#include "rendering.hpp"
#include "director.hpp"
#include "actions.hpp"
#include "node.hpp"
#include "image.hpp"
#include "mutators.hpp"

#ifndef NULL
#define NULL 0
#endif

namespace opi2d
{
    Particle::Particle()
    : pos(0,0), velocity(0,0), acceleration(0,0), friction(1.0),
      rotation(0), rotation_delta(0),
      scale(1.0), scale_delta(0),
      color(1,1,1,1), color_delta(0,0,0,0),
      age(0), life(0), fade_time(0), fade_in(0),
      image(NULL)
    {}
 
    ParticleSystem::ParticleSystem() : last_update(0)
    {
    }
    
    ParticleSystem::~ParticleSystem()
    {
        for(particleset::iterator i=particles.begin(); i != particles.end(); ++i)
        {
            delete (*i);
        }
        particles.clear();
    }
        
    void ParticleSystem::AddParticle(Particle* particle)
    {
        this->particles.insert(particle);
    }
 
    void ParticleSystem::Enter()
    {
        int now = Director::GetInstance()->GetTicker().now;
        bool realtick = Director::GetInstance()->GetTicker().realTick;
        if (this->last_update == 0)
        {
            this->last_update = now;
            return;
        }
        floatval delta = (now - this->last_update) / 1000.0;
        this->last_update = now;
        
        for(mutatorlist::iterator m=mutators.begin(); m != mutators.end(); ++m)
        {
        	(*m)->Mutate(this, delta);
        }
        
        Mat9 tmat;
        quad_vertices va;
        quad_vertices ta;
        quad_colors ca;

        Color color;
        
        RenderingEngine* RE = RenderingEngine::GetInstance();        
        
        for(particleset::iterator i=particles.begin(); i != particles.end(); ++i)
        {
            Particle* p = (*i);
                       
            p->life -= delta;
            p->age += delta;
            if (p->life <= 0)
            {
                to_be_deleted.insert(p);
                continue;
            }
            
            p->velocity += p->acceleration * delta;
            if (realtick)
            {
                p->velocity *= p->friction;
            }
            p->pos += p->velocity * delta;
            
            p->rotation += p->rotation_delta * delta;
            p->scale += p->scale_delta * delta;

            p->color += p->color_delta * delta;
            
            color = p->color;
            if (p->life < p->fade_time)
            {
                float alpha = p->life / p->fade_time;
                color.alpha *= alpha;
            }
            if (p->age < p->fade_in)
            {
                float alpha = p->age / p->fade_in;
                color.alpha *= alpha;
            }
            
            const Image* image = p->image;            
            if (image == NULL) continue;
            
            tmat.identity();
            tmat.translate(p->pos);
            tmat.rotate(p->rotation);
            tmat.scale(p->scale, p->scale);
            
            const Vec2& hotspot = image->hotspot;
            int w = image->w;
            int h = image->h;
            floatval x = -hotspot.x*w;
            floatval y = -hotspot.y*h;

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

            ca.rgba[0] = color;
            ca.rgba[1] = color;
            ca.rgba[2] = color;
            ca.rgba[3] = color;

            RE->AppendQuad(0, image->texid, &va, &ta, &ca);
        }
        
        for(particleset::iterator i=to_be_deleted.begin(); i != to_be_deleted.end(); ++i)
        {
            Particle* p = (*i);
            particles.erase(p);
            delete p;
        }
        to_be_deleted.clear();
    }
    
    void ParticleSystem::AddMutator(Mutator* mutator)
    {
    	this->mutators.push_back(mutator);
    }
  
}
