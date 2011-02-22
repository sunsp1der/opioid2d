class ActionCallbacks
{
public:
    ActionCallbacks();
    virtual ~ActionCallbacks();
    virtual void End()=0;
    virtual void Wake()=0;
};

class Node;

class Action : public Identified
{
public:
    Action();
    virtual ~Action();
    
    void Setup(Node* target, ActionCallbacks* callbacks);
    void SetTimeLimit(double secs);
    
    void Start();
    void End();
    
    void Tick(double delta);
};

class Physics : public Action
{
public:
    Physics();
    virtual ~Physics();

    Vec2 velocity;
    Vec2 acceleration;
    floatval friction;
    floatval rotation;

    void SetRadialVelocity(floatval angle, floatval speed);
    void SetVelocityAngle(floatval angle);
    void SetVelocitySpeed(floatval speed);
        
    Vec2 GetRadialVelocity() const;

};

class IntervalAction : public Action
{
public:
    IntervalAction() {}
    
    void SetInterval(double secs, int repeatMode);
    void SetSmoothing(floatval fadein, floatval fadeout);
    
    double interval_time;
    int repeat_mode;
};


class MoveDelta : public IntervalAction
{
public:
    MoveDelta(const Vec2& delta);
};

class MoveTo : public MoveDelta
{
public:
    MoveTo(const Vec2& pos);
};

class Move : public Action
{
public:
    Move(const Vec2& velocity);
};

class Delay : public Action
{
public:
    Delay(double secs);
};

class AlphaFade : public IntervalAction
{
    public:
    AlphaFade(float dstAlpha);
    void Start();
};

class ColorFade : public IntervalAction
{
    public:
    ColorFade(const Color& color);
    void Start();
};

class RotateDelta : public IntervalAction
{
    public:
    RotateDelta(floatval delta);
    void Start();
};

class Rotate : public Action
{
    public:
    Rotate(floatval speed);
    void Start();
};

class Scale : public Action
{
    public:
    Scale(floatval speed, bool multiply=true);
    void Tick(double delta);
};

class ScaleTo : public IntervalAction
{
	public:
	ScaleTo(const Vec2& dstScale);
	void Start();
};

class TickFunc : public Action
{
    public:
    TickFunc(bool realOnly=false);
    void Tick(double delta);
};

class FollowPath : public Action
{
    public:
    FollowPath(int numpoints, floatval lead, bool alignnode);
    void Start();
    void Tick(double delta);
    
    void SetPoint(int i, const Vec2& pt);
    void SetSpeed(floatval speed);
};

class KeepFacing : public Action
{
   	public:
   	KeepFacing(Node* target, int offset=0);
  	
   	void Tick(double delta);
};

class Animate : public Action
{
	public:
	Animate(double delay);
	void SetDelay(double delay);
	
	void Start();
	void Tick(double delta);	
};


class OrbitAround : public Action
{
	public:
	OrbitAround(Node* center, floatval speed, bool keepAligned);
}; 
