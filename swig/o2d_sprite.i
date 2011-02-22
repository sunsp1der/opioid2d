class Sprite;


class SpriteGroup
{
public:
    SpriteGroup(const std::string& name);
    ~SpriteGroup();
    
    void AddMutator(Mutator* mutator);    
    Sprite* Pick(const Vec2& p) const;
    
    int GetSize() const;
    
    std::vector<Sprite*> ListSprites() const;
};


class Sprite : public Node
{
public:
    Sprite(const Image* image=NULL);
    virtual ~Sprite();
    
    virtual void ReUse();
    
    void JoinGroup(SpriteGroup* group);
    void LeaveGroup(SpriteGroup* group);
    
    void SetImage(const Image* image);
    void EnableLighting(bool flag);

	Sprite* PickSelf(const Vec2& p);
};

