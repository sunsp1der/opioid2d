
#ifndef TICKER_HPP
#define TICKER_HPP

#include "util.hpp"

namespace opi2d
{
    class DLLEXPORT Ticker
    {
        public:
        Ticker(double frequency=25.0);
        
        void Start(int now);
        void Tick(int now);
       
        int now;
        int prevReal;
        int nextReal;
        int realSpan;
       
        double delta;
        double sinceReal;
        bool realTick;
    };
}


#endif

