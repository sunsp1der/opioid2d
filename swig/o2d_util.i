
class DeleteCallback
{
public:
    DeleteCallback();
    virtual ~DeleteCallback();
    
    virtual void OnDelete(int id);
};

class Identified
{
public:
    Identified();
    virtual ~Identified();
    
    unsigned int GetID();
    virtual void ReUse();
    void SetManaged(bool flag);
    
    void Delete();
    bool IsDeleted() const;
    
    static void SetDeleteCallback(DeleteCallback* callback);
};

class Vec2
{
public:
    floatval x,y;

    Vec2();
    Vec2(floatval xval, floatval yval);
    Vec2(const Vec2& other);    

    Vec2& set(floatval x, floatval y);

    Vec2& add(floatval dx, floatval dy);
    Vec2& add(const Vec2& oth);

    Vec2& mul(floatval m);
    Vec2& mul(floatval mx, floatval my);
    Vec2& mul(const Vec2& oth);

    Vec2& operator+=(const Vec2& other);
    Vec2& operator-=(const Vec2& other);
    Vec2& operator*=(const Vec2& other);

    Vec2 operator+(const Vec2& other);
    Vec2 operator-(const Vec2& other);
    Vec2 operator*(floatval mul);

    Vec2 dot(const Vec2& other);
    
    Vec2 rad2xy() const;
    Vec2 xy2rad() const;
    void set_radial(floatval d, floatval l);

    floatval length() const;    
    floatval direction() const;
    void set_length(floatval l);
    void set_direction(floatval d);    

    Vec2 unitvec() const;
    Vec2 ortho() const;
    Vec2 orthounit() const;
    floatval angle(const Vec2& other);
};

class Mat9
{
    public:
    floatval value[9];

	Mat9();    
    Mat9(floatval* src);
    Mat9(const Mat9& other);
  
    floatval get(int index) const;
	void set(int index, floatval val);
	void mul(const Mat9& other);
	
	void translate(floatval x, floatval y);
	void scale(floatval x, floatval y);
	void rotate(floatval angle);
	
	void transform(Vec2& vec) const;
	
    void identity();
    
    Mat9 inversed() const;
};


struct Rect
{
	Vec2 topleft;
	Vec2 size;
	
	Rect();
	Rect(floatval x, floatval y, floatval w, floatval h);
	Rect(const Rect& r);
		
	bool contains(const Vec2& p);
};

struct FreeRect
{
	Vec2 points[4];

	FreeRect();
	FreeRect(const Rect& src);
	
	bool contains(const Vec2& p) const;
};


class Color
{
public:
    float red, green, blue, alpha;
    Color(float red=1.0, float green=1.0, float blue=1.0, float alpha=1.0);
    Color(const Color& oth);
    void set(float red=1.0, float green=1.0, float blue=1.0, float alpha=1.0);

    Color operator*(const Color& oth) const;
    Color operator*(float mult) const;
    Color& operator*=(const Color& oth);
    
    Color operator+(const Color& oth) const;
    Color operator-(const Color& oth) const;
    
    void Apply() const;
};

class Ticker
{
public:
    int now;
    int prevReal;
    int nextReal;
    int realSpan;
   
    double delta;
    double sinceReal;
    bool realTick;    
};


