
class Layer;

class Node : public Identified
{
public:
    Node();
    virtual ~Node();
    
    virtual void ReUse();
    
    void Place(opi2d::Layer* layer);
    Layer* GetLayer() const;
    Layer* GetRootLayer() const;
    
    
    Node* AttachTo(Node* parent, bool back=false);
    Node* Detach();
    
    void OnAttach(Node* child, bool back);
    void OnDetach(Node* child);

    void Traverse(int& zorder);
    void TraverseFree();
    void Enter();
    void EnterFree();


    Sprite* Pick(const Vec2& p);
	Sprite* PickSelf(const Vec2& p);

    Color& GetColor();    
    void SetColor(float r=1, float g=1, float b=1, float a=1);
	void SetColorInheritance(bool flag);
	bool GetColorInheritance() const;
	
	void ToThisFrame(Vec2& p) const;
	void ToParentFrame(Vec2& p) const;
	void FromThisFrame(Vec2& p) const;
	void FromParentFrame(Vec2& p) const;

       
    Vec2& GetPos();
    void SetPos(floatval x, floatval y);
    void AddPos(floatval dx, floatval dy);
       
    const Vec2& GetWorldPos();

	Vec2 GetPosDelta() const;
	Vec2 GetWorldVelocity() const;

    Vec2& GetScale();
    void SetScale(floatval scale);
    void SetScale(const Vec2& scale);
    
    Vec2& GetOffset();
    
    floatval GetRotation();
    void SetRotation(floatval value);
    
    Physics* physics;
};
