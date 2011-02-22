
#include "curve.hpp"

namespace opi2d
{

Curve::Curve(int numpoints, floatval lead) 
    : numpoints(numpoints), segments(0), segment(0), total(0),
      lead(lead), target_pos(0), ready(false),
      finished(false)
{
    this->segments = new Segment[numpoints];
}

Curve::~Curve()
{
    delete this->segments;
}


void Curve::SetPoint(int i, const Vec2& pt)
{
    this->segments[i].pt.set(pt);
}

void Curve::Init()
{
    total = 0;
    segments[0].start = 0;
    segments[0].end = 0;
    segments[0].length = 0;
    
    for(int i=1; i< numpoints; ++i)
    {
        segments[i].start = total;
        segments[i].startpt = segments[i-1].pt;
        segments[i].vec.set(segments[i].pt-segments[i].startpt);
        floatval l = segments[i].vec.length();
        total += l;
        segments[i].length = l;
        segments[i].end = total;
    }
    target_pos = lead;    
    ready = false;
    finished = false;
    segment = segments+1;
}


void Curve::Tick(floatval step, Vec2& pos, floatval& direction, bool setdir)
{
    if (target_pos > total)
    {
        target_pos = total;
        ready = true;
    }
    
    while (target_pos > segment->end)
    {
        ++segment;
    }
    
    floatval rel = (target_pos-segment->start)/segment->length;
    Vec2 target = segment->startpt + segment->vec * rel;
    Vec2 move = target-pos;
    floatval l = move.length();
    
    if (ready && l <= step)
    {
        pos.set(segment->pt);
        finished = true;
    }
    else
    {    
        pos.add(move.unitvec() * step);
    }
    if (setdir) direction = move.direction();
    
    if (!ready)
    {
        if (l < lead*0.1) l = lead*0.1;
        floatval mul = lead/l;        
        target_pos += step * mul;
    }
}

}

