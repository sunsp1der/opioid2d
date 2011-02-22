/*
 * Opioid2D - mutators
 * Copyright (c) 2006 Sami Hangaslammi <shang@iki.fi>
 * 
 * Mutator system for sprite groups and particles.
 * 
 */
 
#ifndef OPIMUTATORS
#define OPIMUTATORS

#include "util.hpp"

#include <vector>

#include "num.hpp"
#include "vec.hpp"

namespace opi2d
{
	class SpriteGroup;
	class ParticleSystem;
	class Area;
	
	class Mutator
	{
		public:
		virtual ~Mutator() {}
		virtual void Mutate(ParticleSystem* system, floatval delta) {}
		virtual void Mutate(SpriteGroup* group, floatval delta) {}
	};
	
	typedef std::vector<Mutator*> mutatorlist;
	
	class LinearForce : public Mutator
	{
		public:
		LinearForce(const Vec2& force);
		void Mutate(ParticleSystem* system, floatval delta);
		void Mutate(SpriteGroup* group, floatval delta);
		
		protected:
		Vec2 force;
	};
	
	class BounceBox : public Mutator
	{
		public:
		BounceBox(int x, int y, int xx, int yy, bool userect=false);
		
		void SetMultipliers(floatval x, floatval y);
		
		void Mutate(ParticleSystem* system, floatval delta);
		void Mutate(SpriteGroup* group, floatval delta);		
		
		protected:
		int x,y,xx,yy;
		bool userect;
		floatval xmul,ymul;
	};
	
	class Zone : public Mutator
	{
		public:
		Zone(Area* area);
		virtual ~Zone();
		
		protected:
		Area* area;
		
	};
	
	class LifeZone : public Zone
	{
		public:
		LifeZone(Area* area) : Zone(area) {}
		void Mutate(ParticleSystem* system, floatval delta);
		void Mutate(SpriteGroup* group, floatval delta);		
	};
	
	class KillZone : public Zone
	{
		public:
		KillZone(Area* area) : Zone(area) {}
		void Mutate(ParticleSystem* system, floatval delta);
		void Mutate(SpriteGroup* group, floatval delta);		
	};
		
	
}

#endif

