
#ifndef OPITEXTURE
#define OPITEXTURE

#include "util.hpp"

namespace opi2d
{
    class DLLEXPORT Texture
    {
        public:
        Texture(int size, bool useFilter=true);
        ~Texture();
        
        void WriteBytes(int x, int y, int w, int h, const char* bytes);
        int GetTexID() const;

        protected:
        
        Texture() {}
        
        int _texid;
    };
}

#endif

