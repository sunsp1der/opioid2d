
#include "ticker.hpp"

namespace opi2d
{
   Ticker::Ticker(double frequency)
     {
	this->realSpan = (int)(1000.0/frequency);
     }
   
   void Ticker::Start(int now)
     {
	this->now = now;
	this->realTick = false;
	this->prevReal = 0;
	this->nextReal = now;
	this->delta = 0.0;
	this->sinceReal = 0.0;
     }
   
   
   void Ticker::Tick(int now)
     {
	int prev = this->now;
	this->now = now;
	this->delta = (now-prev)/1000.0;
	if (now >= this->nextReal)
	  {
	     this->realTick = true;
	     int tmp = this->prevReal;
	     this->prevReal = this->nextReal;
	     this->nextReal = tmp + this->realSpan;
	  }
	else
	  {
	     this->realTick = false;
	  }
	this->sinceReal = (now - this->prevReal) / 1000.0;
     }
}
