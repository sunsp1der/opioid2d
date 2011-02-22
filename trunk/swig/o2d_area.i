
struct Area
{
	virtual bool contains(const Vec2& p) const = 0;
};

struct RectArea : public Area
{
    floatval x,y,xx,yy;
	RectArea(floatval x,floatval y,floatval xx,floatval yy);
	void set(floatval x,floatval y,floatval xx,floatval yy);
	bool contains(const Vec2 &p) const;
};

struct CircleArea : public Area
{
	floatval x, y, radius;
	CircleArea(floatval x, floatval y, floatval radius);
	bool contains(const Vec2 &p) const;
};

struct ArcArea : public Area
{
	floatval x, y, radius, direction, arc;
	ArcArea(floatval x, floatval y, floatval radius, floatval direction, floatval arc);
	bool contains(const Vec2 &p);
};