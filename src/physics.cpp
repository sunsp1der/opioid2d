
#include "physics.hpp"
#include "node.hpp"
#include "director.hpp"
#include "debug.hpp"

namespace opi2d
{
    Physics::~Physics()
    {FUNC
    }
    
    void Physics::Tick(double delta)
    {
        this->velocity += this->acceleration * delta;
        if (Director::GetInstance()->GetTicker().realTick)
        {
            this->velocity *= this->friction;
        }
        target->GetPos() += this->velocity * delta;
        target->SetRotation(target->GetRotation() + this->rotation * delta);
    }
    
    void Physics::Delete()
    {FUNC
    	Identified::Delete();
    }

    void Physics::SetRadialVelocity(floatval angle, floatval speed)
    {
        this->velocity = Vec2(angle,speed).rad2xy();
    }
    
    void Physics::SetVelocityAngle(floatval angle)
    {
        this->SetRadialVelocity(angle, this->velocity.length());
    }
    
    void Physics::SetVelocitySpeed(floatval speed)
    {        
        this->SetRadialVelocity(this->velocity.direction(), speed);
    }
    
    Vec2 Physics::GetRadialVelocity() const
    {
        return this->velocity.xy2rad();
    }
    
}

