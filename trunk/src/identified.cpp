
#include "identified.hpp"
#include "debug.hpp"
#ifndef NULL
#define NULL 0
#endif

namespace opi2d
{
    unsigned int Identified::next_id = 0;
    DeleteCallback* Identified::callback = NULL;
    
    Identified::Identified() : deleted(false), managed(false)
    {FUNC
        this->id = next_id++;        
    }
    
    Identified::~Identified()
    {FUNC
    }
    
    void Identified::ReUse()
    {
        this->deleted = false;
        this->managed = false;
    }
        
    unsigned int Identified::GetID()
    {FUNC
        return id;
    }
    
    void Identified::SetDeleteCallback(DeleteCallback* callback)
    {FUNC
        Identified::callback = callback;
    }
    
    void Identified::Delete()
    {FUNC
        if (this->deleted) return;
        if (!this->managed)
        {
            delete this;
            return;
        }
        this->deleted = true;
        if (callback != NULL)
        {
            callback->OnDelete(id);
        }
    }
}

