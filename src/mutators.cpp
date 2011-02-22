
#include "mutators.hpp"
#include "sprite.hpp"
#include "particles.hpp"
#include "physics.hpp"
#include "util.hpp"
#include "area.hpp"

namespace opi2d
{

	LinearForce::LinearForce(const Vec2& force)
	: force(force)
	{
	}
	
	void LinearForce::Mutate(ParticleSystem* system, floatval delta)
	{
		for(particleset::iterator i=system->particles.begin(); i != system->particles.end(); ++i)
		{
			Particle* p = (*i);
			p->velocity += this->force * delta;
		}
	}

	void LinearForce::Mutate(SpriteGroup* group, floatval delta)
	{		
		for(SpriteSet::iterator i=group->Begin(); i != group->End(); ++i)
		{
			Sprite* s = (*i);
			s->physics->velocity += this->force * delta;
		}
	}
	
	BounceBox::BounceBox(int x, int y, int xx, int yy, bool userect)
	: x(x), y(y), xx(xx), yy(yy), userect(userect), xmul(1.0), ymul(1.0)
	{
	}
	
	void BounceBox::SetMultipliers(floatval x, floatval y)
	{
		this->xmul = x;
		this->ymul = y;
	}	
	
	void BounceBox::Mutate(ParticleSystem* system, floatval delta)
	{
		for(particleset::iterator i=system->particles.begin(); i != system->particles.end(); ++i)
		{
			Particle* p = (*i);
			Vec2& pos = p->pos;
			Vec2& vel = p->velocity;
			if (pos.x <= x)
			{
				pos.x = x;
				if (vel.x < 0) vel.x = -vel.x * this->xmul;
			}
			else if (pos.x >= xx)
			{
				pos.x = xx;
				if (vel.x > 0) vel.x = -vel.x * this->xmul;
			}
			if (pos.y <= y)
			{
				pos.y = y;
				if (vel.y < 0) vel.y = -vel.y * this->ymul;
			}
			else if (pos.y >= yy)
			{
				pos.y = yy;
				if (vel.y > 0) vel.y = -vel.y * this->ymul;
			}
		}
	}
	
	void BounceBox::Mutate(SpriteGroup* group, floatval delta)
	{
		for(SpriteSet::iterator i=group->Begin(); i != group->End(); ++i)
		{
			Sprite* s = (*i);
			Vec2& vel = s->physics->velocity;
			Vec2& pos = s->GetPos();
			if (!userect)
			{
				if (pos.x <= x)
				{
					pos.x = x;
					if (vel.x < 0) vel.x = -vel.x * xmul;;
				}
				else if (pos.x >= xx-1)
				{
					pos.x = xx-1;
					if (vel.x > 0) vel.x = -vel.x * xmul;
				}
				if (pos.y <= y)
				{
					pos.y = y;
					if (vel.y < 0) vel.y = -vel.y * ymul;
				}
				else if (pos.y >= yy-1)
				{
					pos.y = yy-1;
					if (vel.y > 0) vel.y = -vel.y * ymul;
				}
			}
			else
			{
				Rect r = s->GetRect();
				if (r.topleft.x <= x)
				{
					pos.x += (x-r.topleft.x);
					if (vel.x < 0) vel.x = -vel.x * xmul;
				}
				else if (r.topleft.x+r.size.x >= xx-2)
				{
					pos.x += (xx-r.topleft.x-r.size.x-2);
					if (vel.x > 0) vel.x = -vel.x * xmul;
				}
				if (r.topleft.y <= y)
				{
					pos.y += (y-r.topleft.y);
					if (vel.y < 0) vel.y = -vel.y * ymul;
				}
				else if (r.topleft.y+r.size.y > yy-2)
				{
					pos.y += (yy-r.topleft.y-r.size.y-2);
					if (vel.y > 0) vel.y = -vel.y * ymul;
				}
			}
		}
	}

	Zone::Zone(Area* area) : area(area)
	{
	}

	Zone::~Zone()
	{
		delete this->area;
	}
	
	void LifeZone::Mutate(ParticleSystem* system, floatval delta)
	{
		for(particleset::iterator i=system->particles.begin(); i != system->particles.end(); ++i)
		{
			Particle* p = (*i);
			if (!this->area->contains(p->pos))
			{
				p->life = 0;
			}
		}
	}

	void LifeZone::Mutate(SpriteGroup* group, floatval delta)
	{
		for(SpriteSet::iterator i=group->Begin(); i != group->End(); ++i)
		{
			Sprite* s = (*i);
			if (!this->area->contains(s->GetWorldPos()))
			{
				s->Delete();
			}
		}
	}

	void KillZone::Mutate(ParticleSystem* system, floatval delta)
	{
		for(particleset::iterator i=system->particles.begin(); i != system->particles.end(); ++i)
		{
			Particle* p = (*i);
			if (this->area->contains(p->pos))
			{
				p->life = 0;
			}
		}
	}

	void KillZone::Mutate(SpriteGroup* group, floatval delta)
	{
		for(SpriteSet::iterator i=group->Begin(); i != group->End(); ++i)
		{
			Sprite* s = (*i);
			if (this->area->contains(s->GetWorldPos()))
			{
				s->Delete();
			}
		}
	}
	
}
