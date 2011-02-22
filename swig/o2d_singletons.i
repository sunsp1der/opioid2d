template<class T>
class Singleton
{
public:
    static T* GetInstance();
    static void Init();
    static void Destroy();
};

class Director;
class Display;
class SpriteMapper;

%template(DirectorSingleton) Singleton<Director>;
%template(DisplaySingleton) Singleton<Display>;
%template(SpriteMapperSingleton) Singleton<SpriteMapper>;

class SpriteMapper : public Singleton<SpriteMapper>
{
};

class Director : public Singleton<Director>
{
public:
    ~Director();
    
    void Start(int now);
    void Iterate(int now);
    void RenderFrame();
    
    const Ticker& GetTicker() const;
    
    void SetScene(Scene* scene);
    Scene* GetScene();
};

class Display : public Singleton<Display>
{
public:
    void Clear();
    void SetClearColor(const Color& color);
    void EnableClearing(bool flag);
    void InitView(int xres, int yres, int xunits, int yunits);
};
