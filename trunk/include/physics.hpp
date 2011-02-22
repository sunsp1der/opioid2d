
#ifndef OPIPHYSICS
#define OPIPHYSICS

#include "util.hpp"

#include "vec.hpp"
#include "actions.hpp"
#include "num.hpp"

namespace opi2d
{
    class Node;
    
    class DLLEXPORT Physics : public Action
    {
        public:
        Vec2 velocity;
        Vec2 acceleration;
        floatval friction;
        floatval rotation;
        
        Physics() : velocity(0,0), acceleration(0,0), friction(1.0), rotation(0) {}
        virtual ~Physics();
        virtual void Delete();
        
        void Tick(double delta);
            
        void SetRadialVelocity(floatval angle, floatval speed);
        void SetVelocityAngle(floatval angle);
        void SetVelocitySpeed(floatval speed);
            
        Vec2 GetRadialVelocity() const;
        
        protected:
    };
}

#endif

