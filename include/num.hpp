// numeric defines and typedefs
// 

#ifndef OPINUMBERS
#define OPINUMBERS

#include "util.hpp"

#ifdef USE_FLOATS
typedef float floatval;
#else
typedef double floatval;
#endif

#ifndef PI
#define PI (3.141592653589793)
#endif
#define DEG2RAD PI/180.0

#include <cmath>

inline floatval angledir(floatval a, floatval b)
{
    a = fmod(a,(floatval)360.0);
    b = fmod(b,(floatval)360.0);
    floatval delta = b-a;
    if (delta == 0) return 0;
    if (delta > 180)
    {
        return -1;
    }
    else if (delta < -180)
    {
        return 1;
    }
    else if (delta > 0)
    {
        return 1;
    }
    else
    {
        return -1;
    }
}

inline floatval angledelta(floatval a, floatval b)
{
	a = fmod(a,(floatval)360.0);
	b = fmod(b,(floatval)360.0);
    floatval delta = b-a;
    if (delta > 180) return delta-360;
    if (delta < -180) return delta+360;
    return delta;   	
}


#endif

