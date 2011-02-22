/*
 * Opioid2D - identified
 * Copyright (c) 2006 Sami Hangaslammi <shang@iki.fi>
 * 
 * Identified is a utility base-class that is used for memory management.
 * 
 * An "identified" object gets a generated id that is used to track it on
 * the Python side, so that objects returned from the C++ side can always
 * be linked to corresponding Python instance (and also deleted with that
 * instance, so we can utilize Python memory management for identified
 * C++ objects).
 */
#ifndef OPIIDENTIFIED
#define OPIIDENTIFIED

#include "opivm_interface.hpp"

namespace opi2d
{    
    class Identified;
    
    /*
     * DeleteCallback uses the SWIG Director functionality to notify the ObjectManager
     * on the Python side when an identified object is detached from the C++ machinery.
     */
    class DeleteCallback
    {
        public:
        DeleteCallback() {}
        virtual ~DeleteCallback() {}
        
        virtual void OnDelete(int id) {}
    };
    
    class Identified : public VMInterface
    {
        public:
        Identified();
        virtual ~Identified();

		virtual void VM_SetProp(ExecFrame* f, int idx) {}
		virtual void VM_GetProp(ExecFrame* f, int idx) {}
		virtual void VM_MetCall(ExecFrame* f, int idx) {}

        
        /* ReUse resets the object so that the instance can be used again without freeing and
         * reallocating memory.
         */
        virtual void ReUse();
        
        // Notify the Python side about this object's deletion    
        virtual void Delete();
        
        inline bool IsDeleted() const { return deleted; }
        
        /* The managed flag is set to true if this object finalization is
         * the responsibility of Python code.
         * 
         * Otherwise, calling Identified::Delete call this object's destructors
         * and free the memory.
         */
        inline void SetManaged(bool flag) { this->managed = flag; }
        
        unsigned int GetID();
            
        static void SetDeleteCallback(DeleteCallback* callback);
        
        protected:
        unsigned int id;
        bool deleted;
        bool managed;
        
        static unsigned int next_id;
        
        static DeleteCallback* callback;
    };
}

#endif

