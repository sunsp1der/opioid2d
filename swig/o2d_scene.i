
class Sprite;
class Node;

typedef std::list<Node*> Nodes;
typedef std::list<Layer*> Layers;

class SceneCallbacks
{
public:
    SceneCallbacks();
    virtual ~SceneCallbacks();

    virtual void OnCollision(const std::string& group1, const std::string& group2, Sprite* sprite1, Sprite* sprite2);
};

class Layer;

class Camera : public Node
{
public:
  	void ScreenToWorld(Vec2& p) const;
	void ScreenToWorld(Vec2& p, Layer* layer) const;  	
  	void SetAlign(bool flag);
  	bool GetAlign() const;
};


class Light : public Identified
{
public:
    Light();

    Color color;
    floatval intensity;
    floatval cutoff;
    
    Vec2 pos;
    Node* node;
    
    Vec2 worldpos;
    int pos_update_tick;
};


class RenderingPass
{
public:
    RenderingPass();
    
    void SetSrcFunc(int func);
    void SetDstFunc(int func);
};

class Layer
{
public:
    Layer(const std::string& name);
    virtual ~Layer();
    
    const std::string& GetName() const;
    
    void Render();    
    
    void SetFreeForm(bool flag);
    
    void AddNode(Node* node);
    void RemoveNode(Node* node);
    Sprite* Pick(const Vec2& p);
    
    void AddRenderingPass(RenderingPass* pass);
    void ResetRenderingPasses();
    
    void SendNodeToTop(Node* node);
    void SendNodeToBottom(Node* node);
    Nodes GetNodes();
    void SetNodes( Nodes);
    
    floatval camera_offset;
    floatval camera_rotation;
    floatval camera_zoom;
    bool ignore_camera;
};

class SpriteGroup;

class Scene
{
public:
    Scene();
    ~Scene();
    
    void SetCallbacks(SceneCallbacks* callback);
    SceneCallbacks* GetCallbacks();

    SpriteGroup* GetGroup(const std::string& name);
    SpriteGroup* CreateGroup(const std::string& name);
    void EnableCollisions(const std::string& group1, const std::string& group2);
        
    void Tick();
    void RealTick();
    void Render();
    
    void AddLayer(std::string name);
    void DeleteLayer(const std::string& name);
    void DeleteLayer(Layer* layer);
    Layers GetLayers();
    void SetLayers(Layers layers);
    
    Layer* GetLayer(std::string name);
    
    Camera* GetCamera();
    
    void AddLight(Light* light);
    void RemoveLight(Light* light);
    void SetAmbientLight(const Color& color);
    
};
