#include "util.hpp"

#ifdef DARWIN
#include <gl.h>
#else
#include <GL/gl.h>
#endif

#include "texture.hpp"
#include "debug.hpp"

namespace opi2d
{    
    
    Texture::Texture(int size, bool useFilter)
    {FUNC
        GLuint ids[1];
        glGenTextures(1, ids);
        if (glGetError() != GL_NO_ERROR)
        {
            DEBUG("ERROR: Could not generate texture id");
        }
        _texid = ids[0];
        //std::cout << "generated texture id:" << _texid << std::endl;
        glBindTexture(GL_TEXTURE_2D, _texid);
        unsigned char* empty = new unsigned char[size*size*4];
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, size, size, 0, GL_RGBA, GL_UNSIGNED_BYTE, empty);
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP);
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP);
        if (useFilter)
        {
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR);
        }
        else
        {
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST);
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST);
        }
        if (glGetError() != GL_NO_ERROR)
        {
            DEBUG("ERROR: Initializing texture failed");
        }
        delete empty;
    }
    
    Texture::~Texture()
    {FUNC
        GLuint ids[1] = {_texid};
        glDeleteTextures(1, ids);
    }
    
    void Texture::WriteBytes(int x, int y, int w, int h, const char* bytes)
    {FUNC
        glBindTexture(GL_TEXTURE_2D, _texid);
        glTexSubImage2D(GL_TEXTURE_2D, 0, x, y, w, h, GL_RGBA, GL_UNSIGNED_BYTE, bytes);
    }
    
    int Texture::GetTexID() const
    {FUNC
        return _texid;
    }
}
