/*
 * Opioid2D - curve
 * Copyright (c) 2006 Sami Hangaslammi <shang@iki.fi>
 * 
 * Utility class for plotting a smooth path over several anchor points
 * (a bit like bezier curves).
 */
 
#ifndef OPICURVE
#define OPICURVE

#include "util.hpp"

#include "vec.hpp"

namespace opi2d
{
    struct Segment
    {
        Vec2 pt;
        Vec2 startpt;
        Vec2 vec;
        
        floatval length;
        floatval start;
        floatval end;
    };
    
    class Curve
    {
    public:
        Curve(int numpoints, floatval lead);
        ~Curve();
    
        void SetPoint(int i, const Vec2& pt);
        void Init();
        const Segment& GetSegment(int i) const { return segments[i]; }
    
        void Tick(floatval step, Vec2& vec, floatval& direction, bool setdir);
        
        bool IsFinished() const { return finished; }
    
    protected:
        int numpoints;
        Segment* segments;
        Segment* segment;
    
        floatval total;
        floatval lead;
    
        floatval target_pos;
    
        bool ready;
        bool finished;
    };    
    
}

#endif


