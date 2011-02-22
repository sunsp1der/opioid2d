
#include "debug.hpp"
#ifdef DEBUGGING
#include <iostream>
void debugout(const char* file, int line, const char* str)
{
    std::cout << "DEBUG: " <<  file << " " << line << ": " << str << std::endl << std::flush;
}
void debugout(const char* file, int line, int i)
{
    std::cout << "DEBUG: " <<  file << " " << line << ": " << i << std::endl << std::flush;
}
#else
#endif

