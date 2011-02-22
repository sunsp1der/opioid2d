
#ifndef OPIUTIL
#define OPIUTIL

#define DLLEXPORT

//#ifndef O2D_MSVC
#ifndef min
template <class T>
T min(T a, T b)
{
    return (a < b) ? a : b;
}

template <class T>
T max(T a, T b)
{
    return (a > b) ? a : b;
}
#endif
//#endif

#endif

