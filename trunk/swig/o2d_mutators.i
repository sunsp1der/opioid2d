
class SpriteGroup;
class ParticleSystem;

class Mutator
{
};

class LinearForce : public Mutator
{
	public:
	LinearForce(const Vec2& force);
};

class BounceBox : public Mutator
{
	public:
	BounceBox(int x, int y, int xx, int yy, bool userect=false);
	void SetMultipliers(floatval x, floatval y);
};

class Area;

class Zone : public Mutator
{
	public:
	Zone(Area* area);
	virtual ~Zone();
};

class LifeZone : public Zone
{
	public:
	LifeZone(Area* area);
};

class KillZone : public Zone
{
	public:
	KillZone(Area* area);
};
