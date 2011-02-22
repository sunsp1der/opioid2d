
class Texture
{
public:
    Texture(int size, bool useFilter=true);
    ~Texture();
    
    void WriteBytes(int x, int y, int w, int h, const char* bytes);
    int GetTexID() const;
};

class Image
{
public:
    Image(const Texture& tex, int w, int h, float tx, float ty, float txx, float tyy);
    virtual ~Image();
    
    void AddCollisionNode(floatval x, floatval y, floatval width, floatval height);
    void ClearCollisionNodes();

    int texid;
    int w,h;
    float tx,ty,txx,tyy;
    
    Vec2 hotspot;
};

class GridImage : public Image
{
public:
    GridImage(int cols, int rows);
    virtual ~GridImage();
    
    void AppendImage(Image* image);
    void SetSize(int w, int h);
};
