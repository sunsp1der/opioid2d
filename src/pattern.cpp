
#include "util.hpp"

#ifdef DARWIN
#include <gl.h>
#else
#include <GL/gl.h>
#endif

#include "pattern.hpp"
#include "debug.hpp"

namespace opi2d
{
	Pattern::Pattern(int xsize, int ysize, bool useFilter, int hmode, int vmode)
	{
        GLuint ids[1];
        glGenTextures(1, ids);
        if (glGetError() != GL_NO_ERROR)
        {
            DEBUG("ERROR: Could not generate texture id");
        }
        _texid = ids[0];
        glBindTexture(GL_TEXTURE_2D, _texid);
        unsigned char* empty = new unsigned char[xsize*ysize*4];
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, xsize, ysize, 0, GL_RGBA, GL_UNSIGNED_BYTE, empty);
        
        if (hmode == 0)
        {
        	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP);
        }
        else
        {
        	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT);
        }
        if (vmode == 0)
        {
        	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP);
        }
        else
        {
        	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT);
        }
        
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
	
}
